from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_job():
    response = client.post(
        "/jobs",
        json={
            "event_name": "Python Workshop 2026",
            "event_date": "2026-10-08",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "test@example.com"
                },
                {
                    "name": "Another User",
                    "email": "another@example.com"
                }
            ]
        }
    )

    assert response.status_code == 202

    data = response.json()

    assert "job_id" in data
    assert data["status"] == "pending"
    assert data["total"] == 2


def test_job_status():
    response = client.post(
        "/jobs",
        json={
            "event_name": "Status Test 2026",
            "event_date": "2026-10-08",
            "recipients": [
                {
                    "name": "Status User",
                    "email": "status@example.com"
                }
            ]
        }
    )

    assert response.status_code == 202

    job_id = response.json()["job_id"]

    status_response = client.get(f"/jobs/{job_id}")

    assert status_response.status_code == 200

    data = status_response.json()

    assert data["job_id"] == job_id
    assert data["total"] == 1
    assert data["successful"] + data["failed"] == 1
    assert data["progress"] == 100


def test_retrieve_certificates():
    response = client.post(
        "/jobs",
        json={
            "event_name": "Retrieval Test 2026",
            "event_date": "2026-10-08",
            "recipients": [
                {
                    "name": "Retrieval User",
                    "email": "retrieval@example.com"
                }
            ]
        }
    )

    assert response.status_code == 202

    job_id = response.json()["job_id"]

    status_response = client.get(f"/jobs/{job_id}")

    assert status_response.status_code == 200

    data = status_response.json()

    assert data["job_id"] == job_id
    assert data["successful"] == 1

    certificates_response = client.get(
        f"/jobs/{job_id}/certificates"
    )

    assert certificates_response.status_code == 200

    certificates_data = certificates_response.json()

    assert certificates_data["job_id"] == job_id
    assert len(certificates_data["certificates"]) == 1
    assert certificates_data["certificates"][0]["recipient_name"] == "Retrieval User"
    assert "download_url" in certificates_data["certificates"][0]
