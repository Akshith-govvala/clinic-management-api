"""Pydantic schemas for Appointment model."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AppointmentCreate(BaseModel):
    """Schema for creating a new appointment."""

    patient_id: int
    doctor_id: int
    appointment_start: datetime
    appointment_end: datetime


class AppointmentResponse(BaseModel):
    """Schema for appointment response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    doctor_id: int
    appointment_start: datetime
    appointment_end: datetime
