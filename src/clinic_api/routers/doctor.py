"""Doctor API router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from clinic_api.database import get_db
from clinic_api.schemas.doctor import DoctorCreate, DoctorResponse
from clinic_api.services.doctor_service import (
    create_doctor,
    get_doctor,
    get_doctors,
)

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.get("", response_model=list[DoctorResponse])
def read_doctors(db: Session = Depends(get_db)):
    """
    Retrieve all doctors.
    
    Returns:
        List of all doctors in the database.
    """
    return get_doctors(db)


@router.post(
    "",
    response_model=DoctorResponse,
    status_code=201,
)
def add_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new doctor.
    
    Args:
        doctor: Doctor data for creation
        
    Returns:
        The created doctor with assigned ID
    """
    return create_doctor(db, doctor)


@router.get("/{doctor_id}", response_model=DoctorResponse)
def read_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a doctor by ID.
    
    Args:
        doctor_id: ID of the doctor to retrieve
        
    Returns:
        Doctor data if found
        
    Raises:
        HTTPException: If doctor not found (404)
    """
    doctor = get_doctor(db, doctor_id)

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found",
        )

    return doctor
