"""Patient model definition."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from clinic_api.database import Base


class Patient(Base):
    """Patient model for storing patient information."""

    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)

    appointments = relationship(
        "Appointment",
        back_populates="patient",
        cascade="all, delete-orphan"
    )
