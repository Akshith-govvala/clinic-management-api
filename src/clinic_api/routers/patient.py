"""Patient API router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from clinic_api.database import get_db
from clinic_api.schemas.patient import PatientCreate, PatientResponse
from clinic_api.services.patient_service import (
    create_patient,
    get_patient,
    get_patients,
)

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get("", response_model=list[PatientResponse])
def read_patients(db: Session = Depends(get_db)):
    """
    Retrieve all patients.

    Returns:
        List of all patients in the database.
    """
    return get_patients(db)


@router.post(
    "",
    response_model=PatientResponse,
    status_code=201,
)
def add_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new patient.

    Args:
        patient: Patient data for creation

    Returns:
        The created patient with assigned ID
    """
    return create_patient(db, patient)


@router.get("/{patient_id}", response_model=PatientResponse)
def read_patient(
    patient_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a patient by ID.

    Args:
        patient_id: ID of the patient to retrieve

    Returns:
        Patient data if found

    Raises:
        HTTPException: If patient not found (404)
    """
    patient = get_patient(db, patient_id)

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    return patient
