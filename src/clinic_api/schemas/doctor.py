"""Pydantic schemas for Doctor model."""

from pydantic import BaseModel, ConfigDict


class DoctorCreate(BaseModel):
    """Schema for creating a new doctor."""

    name: str
    specialization: str


class DoctorResponse(BaseModel):
    """Schema for doctor response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    specialization: str
