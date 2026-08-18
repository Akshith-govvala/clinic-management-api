"""Database models package."""

from clinic_api.models.appointment import Appointment
from clinic_api.models.doctor import Doctor
from clinic_api.models.patient import Patient

__all__ = ["Patient", "Doctor", "Appointment"]
