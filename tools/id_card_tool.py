from fpdf import FPDF
from PIL import Image
import os

def generate_id_card_pdf(name, id_number, title, organization, profile_pic_path, output_path):
    # ID Card dimensions (e.g., CR80 standard: 3.375 x 2.125 inches = 243 x 153 points approx)
    card_width = 243 # points
    card_height = 153 # points

    pdf = FPDF(unit="pt", format=(card_width, card_height))
    pdf.set_auto_page_break(auto=False, margin=0) # No automatic page breaks
    pdf.add_page()

    # Background (optional - you could have a template image here too)
    # pdf.set_fill_color(220, 220, 220)
    # pdf.rect(0, 0, card_width, card_height, 'F') # Light grey background

    # Header - Organization Name
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(0, 50, 100) # Dark blue
    pdf.cell(0, 20, organization, 0, 1, 'C')
    pdf.ln(5)

    # Profile Picture
    if profile_pic_path and os.path.exists(profile_pic_path):
        try:
            # Open and resize to fit. Example: 70x70 points, centered.
            img_width = 70
            img_height = 70
            x_pos = (card_width - img_width) / 2
            y_pos = pdf.get_y() # Current Y position

            pdf.image(profile_pic_path, x=x_pos, y=y_pos, w=img_width, h=img_height)
            pdf.ln(img_height + 5) # Move cursor below image
        except Exception as e:
            print(f"Error adding profile picture: {e}")
            pdf.ln(img_height + 5) # Still move cursor to avoid overlapping text
    else:
        pdf.ln(75) # Reserve space even if no image

    # Name
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(0, 0, 0) # Black
    pdf.cell(0, 15, name, 0, 1, 'C')

    # Title
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(50, 50, 50) # Dark grey
    pdf.cell(0, 12, title, 0, 1, 'C')
    pdf.ln(5)

    # ID Number
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"ID: {id_number}", 0, 1, 'C')

    # Footer / small print (optional)
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Valid until: N/A", 0, 1, 'C')

    pdf.output(output_path)