from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_invalid_recipient_data():
    response = client.post(
        "/jobs",
        json={
            "event_name": "Python Workshop 2026",
            "event_date": "2026-10-08",
            "recipients": [
                {
                    "name": "A",
                    "email": "invalid-email"
                }
            ]
        }
    )

    assert response.status_code == 422
