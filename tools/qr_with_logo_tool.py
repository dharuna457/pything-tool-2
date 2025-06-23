import qrcode
from PIL import Image
import os

def generate_qr_with_logo(data, logo_path, output_path):
    # Generate the base QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H, # High error correction to embed logo
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path)

        # Calculate position to paste logo in the center
        qr_width, qr_height = img_qr.size
        logo_width, logo_height = logo.size

        # Resize logo if too big for QR code (e.g., 20-30% of QR size)
        max_logo_size = min(qr_width, qr_height) * 0.3
        if logo_width > max_logo_size or logo_height > max_logo_size:
            ratio = min(max_logo_size / logo_width, max_logo_size / logo_height)
            logo = logo.resize((int(logo_width * ratio), int(logo_height * ratio)), Image.Resampling.LANCZOS)
            logo_width, logo_height = logo.size # Update sizes

        pos_x = (qr_width - logo_width) // 2
        pos_y = (qr_height - logo_height) // 2

        # Ensure logo has an alpha channel for transparency if it's a PNG
        if logo.mode in ('RGBA', 'LA') or (logo.mode == 'P' and 'transparency' in logo.info):
            img_qr.paste(logo, (pos_x, pos_y), logo)
        else:
            img_qr.paste(logo, (pos_x, pos_y))

    img_qr.save(output_path)