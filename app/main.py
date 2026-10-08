from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app import crud, models
from app.database import Base, engine, get_db
from app.schemas import JobCreate, JobStatus
from app.services.job_processor import process_job


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bulk Certificate Generator",
    description="API for generating certificates in bulk.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Bulk Certificate Generator API is running"
    }


@app.post("/jobs", status_code=202)
def create_generation_job(
    job_data: JobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    job = crud.create_job(db, job_data)

    background_tasks.add_task(
        process_job,
        job.id,
        job_data.event_name,
        str(job_data.event_date)
    )

    return {
        "job_id": job.id,
        "status": job.status,
        "total": job.total
    }


@app.get("/jobs/{job_id}", response_model=JobStatus)
def get_job_status(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = crud.get_job(db, job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    recipients = crud.get_recipients_by_job(db, job_id)

    progress = 0.0

    if job.total > 0:
        progress = (
            (job.successful + job.failed) / job.total
        ) * 100

    return {
        "job_id": job.id,
        "status": job.status,
        "total": job.total,
        "successful": job.successful,
        "failed": job.failed,
        "progress": progress,
        "recipients": recipients
    }


@app.get("/jobs/{job_id}/certificates")
def get_job_certificates(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = crud.get_job(db, job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    recipients = crud.get_recipients_by_job(db, job_id)

    certificates = []

    for recipient in recipients:
        if recipient.status == "success":
            certificates.append({
                "certificate_id": recipient.id,
                "recipient_name": recipient.name,
                "download_url": (
                    f"/certificates/{recipient.id}"
                )
            })

    return {
        "job_id": job_id,
        "certificates": certificates
    }


@app.get("/certificates/{certificate_id}")
def download_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):
    recipient = (
        db.query(models.Recipient)
        .filter(models.Recipient.id == certificate_id)
        .first()
    )

    if not recipient:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    if recipient.status != "success":
        raise HTTPException(
            status_code=404,
            detail="Certificate was not generated"
        )

    if not recipient.certificate_path:
        raise HTTPException(
            status_code=404,
            detail="Certificate file not found"
        )

    return FileResponse(
        recipient.certificate_path,
        media_type="application/pdf",
        filename=f"certificate_{recipient.id}.pdf"
    )
