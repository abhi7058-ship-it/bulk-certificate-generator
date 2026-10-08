from pathlib import Path

from app.templates.certificate_template import create_certificate_template


OUTPUT_DIR = Path("generated_certificates")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_certificate(
    recipient_id: int,
    recipient_name: str,
    event_name: str,
    event_date: str
) -> str:
    """
    Generate a PDF certificate for one recipient.

    Returns:
        The path of the generated certificate.
    """

    file_name = f"certificate_{recipient_id}.pdf"
    file_path = OUTPUT_DIR / file_name

    create_certificate_template(
        file_path=str(file_path),
        recipient_name=recipient_name,
        event_name=event_name,
        event_date=event_date
    )

    return str(file_path)
