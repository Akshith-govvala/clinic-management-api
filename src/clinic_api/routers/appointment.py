"""Appointment API router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from clinic_api.database import get_db
from clinic_api.schemas.appointment import (
    AppointmentCreate,
    AppointmentResponse,
)
from clinic_api.services.appointment_service import (
    create_appointment,
    get_appointment,
    get_appointments,
)

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)


@router.get("", response_model=list[AppointmentResponse])
def read_appointments(db: Session = Depends(get_db)):
    """
    Retrieve all appointments.

    Returns:
        List of all appointments in the database.
    """
    return get_appointments(db)


@router.post(
    "",
    response_model=AppointmentResponse,
    status_code=201,
)
def add_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new appointment.

    Validates that:
    - Patient exists
    - Doctor exists
    - Appointment end time is after start time
    - No overlapping appointments for the doctor

    Args:
        appointment: Appointment data for creation

    Returns:
        The created appointment with assigned ID

    Raises:
        HTTPException: If validation fails
    """
    return create_appointment(db, appointment)


@router.get(
    "/{appointment_id}",
    response_model=AppointmentResponse,
)
def read_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve an appointment by ID.

    Args:
        appointment_id: ID of the appointment to retrieve

    Returns:
        Appointment data if found

    Raises:
        HTTPException: If appointment not found (404)
    """
    appointment = get_appointment(
        db,
        appointment_id,
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found",
        )

    return appointment
