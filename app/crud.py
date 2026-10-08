from sqlalchemy.orm import Session

from app import models
from app.schemas import JobCreate


def create_job(db: Session, job_data: JobCreate):
    job = models.Job(
        status="pending",
        total=len(job_data.recipients),
        successful=0,
        failed=0
    )

    db.add(job)
    db.flush()

    for recipient_data in job_data.recipients:
        recipient = models.Recipient(
            job_id=job.id,
            name=recipient_data.name,
            email=recipient_data.email,
            status="pending"
        )
        db.add(recipient)

    db.commit()
    db.refresh(job)

    return job


def get_job(db: Session, job_id: int):
    return (
        db.query(models.Job)
        .filter(models.Job.id == job_id)
        .first()
    )


def get_recipients_by_job(db: Session, job_id: int):
    return (
        db.query(models.Recipient)
        .filter(models.Recipient.job_id == job_id)
        .all()
    )
