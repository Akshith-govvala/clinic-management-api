"""Doctor service - business logic for doctor operations."""

from sqlalchemy.orm import Session

from clinic_api.models.doctor import Doctor


def get_doctors(db: Session):
    """Retrieve all doctors from database."""
    return db.query(Doctor).all()


def get_doctor(db: Session, doctor_id: int):
    """Retrieve a specific doctor by ID."""
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()


def create_doctor(db: Session, doctor_data):
    """Create a new doctor in the database."""
    doctor = Doctor(**doctor_data.model_dump())

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return doctor
