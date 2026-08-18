"""Pydantic schemas for Patient model."""

from pydantic import BaseModel, ConfigDict, EmailStr


class PatientCreate(BaseModel):
    """Schema for creating a new patient."""

    name: str
    email: EmailStr
    phone: str


class PatientResponse(BaseModel):
    """Schema for patient response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    phone: str
