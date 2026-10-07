from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base


class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id = Column(Integer, primary_key=True, index=True)

    event_name = Column(String, nullable=False)
    event_date = Column(String, nullable=False)

    status = Column(String, default="PENDING")

    total_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    recipients = relationship(
        "Recipient",
        back_populates="job",
        cascade="all, delete-orphan"
    )


class Recipient(Base):
    __tablename__ = "recipients"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(
        Integer,
        ForeignKey("generation_jobs.id"),
        nullable=False
    )

    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

    status = Column(String, default="PENDING")

    certificate_path = Column(String, nullable=True)
    error_message = Column(String, nullable=True)

    job = relationship(
        "GenerationJob",
        back_populates="recipients"
    )