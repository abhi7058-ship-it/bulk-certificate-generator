# Bulk Certificate Generator

A REST API for generating participation certificates in bulk for multiple recipients using a predefined certificate template.

The application accepts a single bulk request, validates recipient data, creates a background generation job, generates individual PDF certificates, tracks progress, handles individual failures, and provides certificate download endpoints.

## Features

- Bulk certificate generation
- Recipient data validation
- Predefined PDF certificate template
- Background job processing
- Job status and progress tracking
- Individual recipient success/failure tracking
- Individual certificate retrieval
- Failure isolation so one failed certificate does not stop the remaining certificates
- Automated tests using pytest

## Tech Stack

- Python 3.14
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- ReportLab
- Pytest

## Project Structure

```text
bulk-certificate-generator/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── certificate_generator.py
│   │   └── job_processor.py
│   │
│   └── templates/
│       ├── __init__.py
│       └── certificate_template.py
│
├── generated_certificates/
│
├── tests/
│   ├── __init__.py
│   ├── test_jobs.py
│   ├── test_validation.py
│   ├── test_certificate_generation.py
│   └── test_failures.py
│
├── .gitignore
├── README.md
├── requirements.txt
└── certificate.db
