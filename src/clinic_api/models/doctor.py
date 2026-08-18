"""Doctor model definition."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from clinic_api.database import Base


class Doctor(Base):
    """Doctor model for storing doctor information."""

    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)

    appointments = relationship(
        "Appointment",
        back_populates="doctor",
        cascade="all, delete-orphan"
    )
