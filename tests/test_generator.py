from app.services.certificate_generator import generate_certificate
import os


def test_certificate_generation(tmp_path, monkeypatch):

    monkeypatch.setattr(
        "app.services.certificate_generator.OUTPUT_DIR",
        str(tmp_path)
    )

    file_path = generate_certificate(
        certificate_id=1,
        recipient_name="Rahul Kumar",
        event_name="Python Workshop",
        event_date="10 October 2026"
    )

    assert os.path.exists(file_path)
    assert file_path.endswith(".pdf")