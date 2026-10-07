# Bulk Certificate Generator

A backend API that accepts a bulk list of recipients and generates participation
certificates using a predefined certificate template.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- ReportLab
- Pytest

## Project Setup 

 1. Clone the project

<!-- ```bash -->
    git clone <your-repository-url>
    cd bulk-certificate-generator

2. Create virtual environment
    python -m venv venv

3. Install dependencies
    pip install -r requirements.txt

4. Configure database
    Create a PostgreSQL database named:
certificate_generator



Create .env file:
    DATABASE_URL=postgresql://postgres:your_password@localhost:5432/certificate_generator



Run the Application:
    uvicorn app.main:app --reload

The API will run at:
   http://127.0.0.1:8000

Swagger API documentation:
   http://127.0.0.1:8000/docs




Create Generation Job
Send a POST request to:
POST /api/v1/jobs

Example:
{
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

The API returns a job ID:
{
  "job_id": 1,
  "status": "PENDING",
  "total": 2
}

Check Job Status
Use:
GET /api/v1/jobs/{job_id}

Example:
GET /api/v1/jobs/1

The response contains:
- Job status
- Total recipients
- Successful certificates
- Failed certificates
- Individual recipient status
Retrieve Certificate
After successful generation, use:
GET /api/v1/certificates/{certificate_id}

Example:
GET /api/v1/certificates/1

This returns the generated PDF certificate.
Generated certificates are stored in:
generated_certificates/

Run Tests
Run:
pytest -v
