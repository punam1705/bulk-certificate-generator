from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_job():

    response = client.post(
        "/api/v1/jobs",
        json={
            "event_name": "Python Workshop",
            "event_date": "10 October 2026",
            "recipients": [
                {
                    "name": "Rahul Kumar",
                    "email": "rahul@gmail.com"
                },
                {
                    "name": "Priya Singh",
                    "email": "priya@gmail.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "job_id" in data
    assert data["total"] == 2
    assert data["status"] == "PENDING"


def test_invalid_email():

    response = client.post(
        "/api/v1/jobs",
        json={
            "event_name": "Python Workshop",
            "event_date": "10 October 2026",
            "recipients": [
                {
                    "name": "Rahul Kumar",
                    "email": "invalid-email"
                }
            ]
        }
    )

    assert response.status_code == 422

def test_empty_recipients():

    response = client.post(
        "/api/v1/jobs",
        json={
            "event_name": "Python Workshop",
            "event_date": "10 October 2026",
            "recipients": []
        }
    )

    assert response.status_code == 422

def test_job_status():

    create_response = client.post(
        "/api/v1/jobs",
        json={
            "event_name": "Python Workshop",
            "event_date": "10 October 2026",
            "recipients": [
                {
                    "name": "Rahul Kumar",
                    "email": "rahul@gmail.com"
                }
            ]
        }
    )

    job_id = create_response.json()["job_id"]

    response = client.get(
        f"/api/v1/jobs/{job_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["job_id"] == job_id
    assert data["total"] == 1


def test_individual_certificate_failure():

    response = client.post(
        "/api/v1/jobs",
        json={
            "event_name": "Python Workshop",
            "event_date": "10 October 2026",
            "recipients": [
                {
                    "name": "Rahul Kumar",
                    "email": "rahul@gmail.com"
                },
                {
                    "name": "FAIL",
                    "email": "fail@gmail.com"
                },
                {
                    "name": "Aman Kumar",
                    "email": "aman@gmail.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    job_id = response.json()["job_id"]

    response = client.get(
        f"/api/v1/jobs/{job_id}"
    )

    data = response.json()

    assert data["total"] == 3
    assert data["successful"] == 2
    assert data["failed"] == 1