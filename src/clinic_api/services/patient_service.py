"""Patient service - business logic for patient operations."""

from sqlalchemy.orm import Session

from clinic_api.models.patient import Patient


def get_patients(db: Session):
    """Retrieve all patients from database."""
    return db.query(Patient).all()


def get_patient(db: Session, patient_id: int):
    """Retrieve a specific patient by ID."""
    return db.query(Patient).filter(Patient.id == patient_id).first()


def create_patient(db: Session, patient_data):
    """Create a new patient in the database."""
    patient = Patient(**patient_data.model_dump())

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient
