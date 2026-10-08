from pathlib import Path

from app.services.certificate_generator import generate_certificate


def test_certificate_generation(tmp_path):
    output_dir = tmp_path

    certificate_path = output_dir / "certificate_999.pdf"

    from app.services import certificate_generator

    original_output_dir = certificate_generator.OUTPUT_DIR
    certificate_generator.OUTPUT_DIR = output_dir

    try:
        result = generate_certificate(
            recipient_id=999,
            recipient_name="Test User",
            event_name="Python Workshop 2026",
            event_date="2026-10-08"
        )

        assert result == str(certificate_path)
        assert Path(result).exists()
        assert Path(result).stat().st_size > 0

    finally:
        certificate_generator.OUTPUT_DIR = original_output_dir
