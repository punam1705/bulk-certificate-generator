from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from ..database import SessionLocal, get_db
from ..models import GenerationJob, Recipient
from ..schemas import GenerationJobCreate
from ..services.certificate_generator import generate_certificate


router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Jobs"]
)


def process_job(job_id: int):

    db = SessionLocal()

    try:

        job = db.query(
            GenerationJob
        ).filter(
            GenerationJob.id == job_id
        ).first()

        if not job:
            return

        job.status = "PROCESSING"
        db.commit()

        for recipient in job.recipients:

            try:

                path = generate_certificate(
                    recipient.id,
                    recipient.name,
                    job.event_name,
                    job.event_date
                )

                recipient.status = "SUCCESS"
                recipient.certificate_path = path

                job.success_count += 1

            except Exception as e:

                recipient.status = "FAILED"
                recipient.error_message = str(e)

                job.failed_count += 1

            db.commit()

        job.status = "COMPLETED"

        db.commit()

    finally:
        db.close()


@router.post("")
def create_job(
    request: GenerationJobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    job = GenerationJob(
        event_name=request.event_name,
        event_date=request.event_date,
        total_count=len(request.recipients),
        status="PENDING"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    for item in request.recipients:

        recipient = Recipient(
            job_id=job.id,
            name=item.name,
            email=item.email,
            status="PENDING"
        )

        db.add(recipient)

    db.commit()

    background_tasks.add_task(
        process_job,
        job.id
    )

    return {
        "job_id": job.id,
        "status": "PENDING",
        "total": job.total_count
    }

@router.get("/{job_id}")
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):

    job = (
        db.query(GenerationJob)
        .filter(GenerationJob.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    recipients = []

    for recipient in job.recipients:

        data = {
            "id": recipient.id,
            "name": recipient.name,
            "email": recipient.email,
            "status": recipient.status
        }

        if recipient.status == "SUCCESS":
            data["certificate_id"] = recipient.id

        if recipient.status == "FAILED":
            data["error"] = recipient.error_message

        recipients.append(data)

    return {
        "job_id": job.id,
        "event_name": job.event_name,
        "event_date": job.event_date,
        "status": job.status,
        "total": job.total_count,
        "successful": job.success_count,
        "failed": job.failed_count,
        "recipients": recipients
    }
