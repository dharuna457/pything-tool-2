from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import date

def generate_quotation_pdf(company_name, client_name, item_description, amount, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles for a professional look
    title_style = ParagraphStyle(
        'Title',
        parent=styles['h1'],
        fontSize=28,
        leading=34,
        alignment=1, # Center
        spaceAfter=20,
        textColor=colors.HexColor('#0056b3'),
        fontName='Helvetica-Bold'
    )

    sub_heading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['h2'],
        fontSize=18,
        leading=22,
        spaceAfter=10,
        textColor=colors.HexColor('#333333'),
        fontName='Helvetica-Bold'
    )

    normal_style = styles['Normal']
    normal_style.fontSize = 12
    normal_style.leading = 14
    normal_style.fontName = 'Helvetica'

    # Invoice/Quotation number placeholder
    story.append(Paragraph("QUOTATION", title_style))
    story.append(Paragraph(f"<b>Quotation Date:</b> {date.today().strftime('%B %d, %Y')}", normal_style))
    story.append(Spacer(1, 0.4 * inch))

    # Company Info (sender)
    story.append(Paragraph("<b>From:</b>", sub_heading_style))
    story.append(Paragraph(company_name, normal_style))
    story.append(Spacer(1, 0.2 * inch))

    # Client Info (recipient)
    story.append(Paragraph("<b>To:</b>", sub_heading_style))
    story.append(Paragraph(client_name, normal_style))
    story.append(Spacer(1, 0.4 * inch))

    # Item Details
    story.append(Paragraph("<b><u>Quotation Details:</u></b>", sub_heading_style))
    story.append(Spacer(1, 0.1 * inch))

    # Use a table or just paragraphs for simple layout
    story.append(Paragraph(f"<b>Description:</b> {item_description}", normal_style))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(f"<b>Amount:</b> ${amount:,.2f}", normal_style))
    story.append(Spacer(1, 0.5 * inch))

    # Terms and Conditions (Optional)
    story.append(Paragraph("<b><u>Terms & Conditions:</u></b>", sub_heading_style))
    story.append(Paragraph("1. Payment due within 30 days of invoice date.", normal_style))
    story.append(Paragraph("2. All prices are in USD.", normal_style))
    story.append(Spacer(1, 0.5 * inch))


    # Signature Line
    story.append(Paragraph("_________________________", normal_style))
    story.append(Paragraph("Authorized Signature", normal_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(company_name, normal_style))


    doc.build(story)