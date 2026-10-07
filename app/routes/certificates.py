from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Recipient


router = APIRouter(
    prefix="/api/v1/certificates",
    tags=["Certificates"]
)


@router.get("/{certificate_id}")
def get_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):

    recipient = db.query(
        Recipient
    ).filter(
        Recipient.id == certificate_id
    ).first()

    if not recipient:
        raise HTTPException(
        status_code=404,
        detail="Certificate not found"
    )

    if recipient.status != "SUCCESS":
        return {
            "error": "Certificate is not available"
        }

    return FileResponse(
        recipient.certificate_path,
        media_type="application/pdf",
        filename=f"certificate_{certificate_id}.pdf"
    )