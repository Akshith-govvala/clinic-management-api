"""FastAPI application entry point."""

from fastapi import FastAPI

# Import models to register them with Base.metadata
from clinic_api.models import Appointment, Doctor, Patient  # noqa: F401
from clinic_api.routers.appointment import router as appointment_router
from clinic_api.routers.doctor import router as doctor_router
from clinic_api.routers.patient import router as patient_router

app = FastAPI(
    title="Clinic Management API",
    description="Hospital Appointment Management System",
    version="0.1.0",
)

# Include routers
app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(appointment_router)


@app.get("/")
def read_root():
    """Root endpoint for API health check."""
    return {"message": "Clinic Management API", "version": "0.1.0", "status": "running"}
