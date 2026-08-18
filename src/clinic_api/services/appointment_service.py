"""Appointment service - business logic for appointment operations."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from clinic_api.models.appointment import Appointment
from clinic_api.models.doctor import Doctor
from clinic_api.models.patient import Patient


def get_appointments(db: Session):
    """Retrieve all appointments from database."""
    return db.query(Appointment).all()


def get_appointment(db: Session, appointment_id: int):
    """Retrieve a specific appointment by ID."""
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def create_appointment(db: Session, appointment_data):
    """
    Create a new appointment with validation.

    Validates:
    - Patient exists
    - Doctor exists
    - Appointment end time is after start time
    - No overlapping appointments for the doctor
    """
    # Validate time range
    if appointment_data.appointment_start >= appointment_data.appointment_end:
        raise HTTPException(
            status_code=400,
            detail="Appointment end time must be after start time",
        )

    # Check patient exists
    patient = (
        db.query(Patient).filter(Patient.id == appointment_data.patient_id).first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    # Check doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == appointment_data.doctor_id).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found",
        )

    # Check overlapping appointments for the same doctor
    # Condition: existing_start < new_end AND existing_end > new_start
    overlap = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == appointment_data.doctor_id,
            Appointment.appointment_start < appointment_data.appointment_end,
            Appointment.appointment_end > appointment_data.appointment_start,
        )
        .first()
    )

    if overlap:
        raise HTTPException(
            status_code=400,
            detail="Appointment overlaps with existing appointment for this doctor",
        )

    # Create the appointment
    appointment = Appointment(
        patient_id=appointment_data.patient_id,
        doctor_id=appointment_data.doctor_id,
        appointment_start=appointment_data.appointment_start,
        appointment_end=appointment_data.appointment_end,
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment
