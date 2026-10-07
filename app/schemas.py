from pydantic import BaseModel, EmailStr, Field
from typing import List


class RecipientCreate(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr


class GenerationJobCreate(BaseModel):
    event_name: str = Field(min_length=2)
    event_date: str
    recipients: List[RecipientCreate] = Field(min_length=1)