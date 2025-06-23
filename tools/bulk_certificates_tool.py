from fpdf import FPDF
from PIL import Image
import csv
import os
import zipfile
import uuid

def generate_bulk_certificates(template_image_path, csv_data_path, output_zip_path):
    if not os.path.exists(template_image_path):
        raise FileNotFoundError(f"Certificate template image not found: {template_image_path}")
    if not os.path.exists(csv_data_path):
        raise FileNotFoundError(f"CSV data file not found: {csv_data_path}")

    # Ensure image is RGB for PDF compatibility
    try:
        template_img = Image.open(template_image_path).convert('RGB')
        temp_template_path_rgb = template_image_path.replace('.png', '_rgb.png').replace('.jpg', '_rgb.jpg')
        template_img.save(temp_template_path_rgb)
    except Exception as e:
        raise ValueError(f"Could not process template image: {e}")

    certificate_files = []
    temp_dir = os.path.join(os.path.dirname(output_zip_path), f"temp_certs_{uuid.uuid4().hex}")
    os.makedirs(temp_dir, exist_ok=True)

    try:
        with open(csv_data_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            # Expected CSV headers: 'Name', 'Course', 'Date' (or similar, adjust below)
            for row_num, row in enumerate(reader):
                try:
                    name = row.get('Name', '').strip()
                    course = row.get('Course', '').strip()
                    date_issued = row.get('Date', '').strip()

                    if not all([name, course, date_issued]):
                        print(f"Skipping row {row_num + 2} due to missing data: {row}") # +2 for header and 0-index
                        continue # Skip rows with incomplete data

                    pdf = FPDF(unit="pt", format="Letter") # Assuming Letter size
                    pdf.add_page()

                    # Add template image as background
                    pdf.image(temp_template_path_rgb, x=0, y=0, w=pdf.w, h=pdf.h)

                    # Set font for text on certificate
                    pdf.set_font("Helvetica", "B", 36)
                    pdf.set_text_color(0, 0, 0) # Black color

                    # Add Recipient Name (adjust positioning as needed)
                    pdf.set_xy(0, pdf.h / 2 - 50) # Center vertically, adjust for name
                    pdf.cell(w=pdf.w, h=20, text=name, align='C')

                    # Add Course/Achievement
                    pdf.set_font("Helvetica", "", 24)
                    pdf.set_xy(0, pdf.h / 2 + 10) # Below name
                    pdf.cell(w=pdf.w, h=20, text=f"for completing the {course}", align='C')

                    # Add Date (adjust positioning)
                    pdf.set_font("Helvetica", "", 16)
                    pdf.set_xy(0, pdf.h - 100) # Near bottom
                    pdf.cell(w=pdf.w, h=20, text=f"Issued on {date_issued}", align='C')

                    # Save each certificate
                    certificate_filename = f"certificate_{name.replace(' ', '_')}_{uuid.uuid4().hex[:4]}.pdf"
                    certificate_path = os.path.join(temp_dir, certificate_filename)
                    pdf.output(certificate_path)
                    certificate_files.append(certificate_path)

                except Exception as e:
                    print(f"Error processing row {row_num + 2}: {row}. Error: {e}")
                    # Continue to next row even if one fails

        if not certificate_files:
            raise ValueError("No certificates were generated. Check CSV format and data.")

        # Zip all generated certificates
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in certificate_files:
                zipf.write(file_path, os.path.basename(file_path))

    finally:
        # Clean up temporary RGB template image
        if os.path.exists(temp_template_path_rgb):
            os.remove(temp_template_path_rgb)
        # Clean up temporary individual certificate PDFs
        for f in certificate_files:
            if os.path.exists(f):
                os.remove(f)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)