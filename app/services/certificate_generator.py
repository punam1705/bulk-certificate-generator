from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import os


OUTPUT_DIR = "generated_certificates"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_certificate(
    certificate_id: int,
    recipient_name: str,
    event_name: str,
    event_date: str
):
    
    file_path = os.path.join(
        OUTPUT_DIR,
        f"certificate_{certificate_id}.pdf"
    )
    if recipient_name == "FAIL":
        raise Exception("Certificate generation failed")

    width, height = A4

    pdf = canvas.Canvas(file_path, pagesize=A4)


    pdf.rect(
        20 * mm,
        20 * mm,
        width - 40 * mm,
        height - 40 * mm
    )

    pdf.setFont("Helvetica-Bold", 28)

    pdf.drawCentredString(
        width / 2,
        height - 80 * mm,
        "CERTIFICATE"
    )

    pdf.setFont("Helvetica", 18)

    pdf.drawCentredString(
        width / 2,
        height - 95 * mm,
        "OF PARTICIPATION"
    )

    pdf.setFont("Helvetica", 14)

    pdf.drawCentredString(
        width / 2,
        height - 120 * mm,
        "This certificate is proudly presented to"
    )

    pdf.setFont("Helvetica-Bold", 24)

    pdf.drawCentredString(
        width / 2,
        height - 140 * mm,
        recipient_name
    )

    pdf.setFont("Helvetica", 14)

    pdf.drawCentredString(
        width / 2,
        height - 160 * mm,
        f"for participating in {event_name}"
    )

    pdf.drawCentredString(
        width / 2,
        height - 175 * mm,
        f"Date: {event_date}"
    )

    pdf.save()

    return file_path