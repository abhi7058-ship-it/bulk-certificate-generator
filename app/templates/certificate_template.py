from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


def create_certificate_template(
    file_path: str,
    recipient_name: str,
    event_name: str,
    event_date: str
):
    pdf = canvas.Canvas(file_path, pagesize=A4)

    width, height = A4

    # Border
    pdf.setLineWidth(3)
    pdf.rect(
        15 * mm,
        15 * mm,
        width - 30 * mm,
        height - 30 * mm
    )

    # Title
    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(
        width / 2,
        height - 65 * mm,
        "CERTIFICATE"
    )

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(
        width / 2,
        height - 80 * mm,
        "OF PARTICIPATION"
    )

    # Introductory text
    pdf.setFont("Helvetica", 13)
    pdf.drawCentredString(
        width / 2,
        height - 105 * mm,
        "This is to certify that"
    )

    # Recipient name
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(
        width / 2,
        height - 125 * mm,
        recipient_name
    )

    # Event information
    pdf.setFont("Helvetica", 13)
    pdf.drawCentredString(
        width / 2,
        height - 150 * mm,
        f"has successfully participated in {event_name}"
    )

    pdf.drawCentredString(
        width / 2,
        height - 165 * mm,
        f"held on {event_date}"
    )

    # Signature
    pdf.line(
        width / 2 - 35 * mm,
        height - 205 * mm,
        width / 2 + 35 * mm,
        height - 205 * mm
    )

    pdf.setFont("Helvetica", 11)
    pdf.drawCentredString(
        width / 2,
        height - 212 * mm,
        "Authorized Signature"
    )

    pdf.save()
