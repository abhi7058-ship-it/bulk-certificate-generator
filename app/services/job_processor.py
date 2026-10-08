from datetime import datetime, UTC

from app.database import SessionLocal
from app import models
from app.services.certificate_generator import generate_certificate


def process_job(
    job_id: int,
    event_name: str,
    event_date: str
):
    """
    Process all recipients belonging to a generation job.

    Each recipient is processed independently so that
    one failure does not stop the remaining recipients.
    """

    db = SessionLocal()

    try:
        job = (
            db.query(models.Job)
            .filter(models.Job.id == job_id)
            .first()
        )

        if not job:
            return

        job.status = "processing"
        db.commit()

        recipients = (
            db.query(models.Recipient)
            .filter(models.Recipient.job_id == job_id)
            .all()
        )

        for recipient in recipients:
            try:
                certificate_path = generate_certificate(
                    recipient_id=recipient.id,
                    recipient_name=recipient.name,
                    event_name=event_name,
                    event_date=event_date
                )

                recipient.status = "success"
                recipient.certificate_path = certificate_path
                recipient.error_message = None

                job.successful += 1

            except Exception as error:
                recipient.status = "failed"
                recipient.error_message = str(error)

                job.failed += 1

            db.commit()

        job.status = "completed"
        job.completed_at = datetime.now(UTC)

        db.commit()

    except Exception:
        job.status = "failed"
        db.commit()

    finally:
        db.close()
