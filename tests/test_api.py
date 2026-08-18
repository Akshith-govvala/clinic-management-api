"""Comprehensive test suite for Clinic Management API."""

from datetime import datetime, timedelta, timezone

from .conftest import client


class TestPatientAPI:
    """Test suite for Patient endpoints."""

    def test_create_patient(self):
        """Test creating a new patient."""
        response = client.post(
            "/patients",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "1234567890"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert data["phone"] == "1234567890"
        assert "id" in data

    def test_create_patient_invalid_email(self):
        """Test creating a patient with invalid email."""
        response = client.post(
            "/patients",
            json={
                "name": "Jane Doe",
                "email": "invalid-email",
                "phone": "1234567890"
            }
        )

        assert response.status_code == 422  # Validation error

    def test_get_all_patients(self):
        """Test retrieving all patients."""
        # Create a patient first
        client.post(
            "/patients",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "1234567890"
            }
        )

        response = client.get("/patients")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["name"] == "John Doe"

    def test_get_all_patients_empty(self):
        """Test retrieving patients when none exist."""
        response = client.get("/patients")

        assert response.status_code == 200
        assert response.json() == []

    def test_get_patient_by_id(self):
        """Test retrieving a patient by ID."""
        # Create a patient first
        create_response = client.post(
            "/patients",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "1234567890"
            }
        )
        patient_id = create_response.json()["id"]

        response = client.get(f"/patients/{patient_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == patient_id
        assert data["name"] == "John Doe"

    def test_get_patient_not_found(self):
        """Test retrieving a non-existent patient."""
        response = client.get("/patients/9999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Patient not found"


class TestDoctorAPI:
    """Test suite for Doctor endpoints."""

    def test_create_doctor(self):
        """Test creating a new doctor."""
        response = client.post(
            "/doctors",
            json={
                "name": "Dr. Smith",
                "specialization": "Cardiology"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Dr. Smith"
        assert data["specialization"] == "Cardiology"
        assert "id" in data

    def test_get_all_doctors(self):
        """Test retrieving all doctors."""
        # Create a doctor first
        client.post(
            "/doctors",
            json={
                "name": "Dr. Smith",
                "specialization": "Cardiology"
            }
        )

        response = client.get("/doctors")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["name"] == "Dr. Smith"

    def test_get_all_doctors_empty(self):
        """Test retrieving doctors when none exist."""
        response = client.get("/doctors")

        assert response.status_code == 200
        assert response.json() == []

    def test_get_doctor_by_id(self):
        """Test retrieving a doctor by ID."""
        # Create a doctor first
        create_response = client.post(
            "/doctors",
            json={
                "name": "Dr. Smith",
                "specialization": "Cardiology"
            }
        )
        doctor_id = create_response.json()["id"]

        response = client.get(f"/doctors/{doctor_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == doctor_id
        assert data["name"] == "Dr. Smith"

    def test_get_doctor_not_found(self):
        """Test retrieving a non-existent doctor."""
        response = client.get("/doctors/9999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Doctor not found"


class TestAppointmentAPI:
    """Test suite for Appointment endpoints."""

    def get_test_data(self):
        """Create test data for each test."""
        # Create a patient
        patient_response = client.post(
            "/patients",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "1234567890"
            }
        )
        patient_id = patient_response.json()["id"]

        # Create a doctor
        doctor_response = client.post(
            "/doctors",
            json={
                "name": "Dr. Smith",
                "specialization": "Cardiology"
            }
        )
        doctor_id = doctor_response.json()["id"]
        
        return patient_id, doctor_id

    def test_create_appointment_success(self):
        """Test successfully creating an appointment."""
        patient_id, doctor_id = self.get_test_data()
        
        start_time = datetime.now(timezone.utc) + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)

        response = client.post(
            "/appointments",
            json={
                "patient_id": patient_id,
                "doctor_id": doctor_id,
                "appointment_start": start_time.isoformat(),
                "appointment_end": end_time.isoformat()
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["patient_id"] == patient_id
        assert data["doctor_id"] == doctor_id
        assert "id" in data

    def test_create_appointment_invalid_time_range(self):
        """Test creating appointment with end time before start time."""
        start_time = datetime.now(timezone.utc) + timedelta(days=1)
        end_time = start_time - timedelta(hours=1)

        response = client.post(
            "/appointments",
            json={
                "patient_id": self.patient_id,
                "doctor_id": self.doctor_id,
                "appointment_start": start_time.isoformat(),
                "appointment_end": end_time.isoformat()
            }
        )

        assert response.status_code == 400
        assert "end time must be after start time" in response.json()["detail"]

    def test_create_appointment_same_start_end_time(self):
        """Test creating appointment with same start and end time."""
        start_time = datetime.now(timezone.utc) + timedelta(days=1)

        response = client.post(
            "/appointments",
            json={
                "patient_id": self.patient_id,
                "doctor_id": self.doctor_id,
                "appointment_start": start_time.isoformat(),
                "appointment_end": start_time.isoformat()
            }
        )

        assert response.status_code == 400

    def test_create_appointment_patient_not_found(self):
        """Test creating appointment with non-existent patient."""
        start_time = datetime.now(timezone.utc) + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)

        response = client.post(
            "/appointments",
            json={
                "patient_id": 9999,
                "doctor_id": self.doctor_id,
                "appointment_start": start_time.isoformat(),
                "appointment_end": end_time.isoformat()
            }
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Patient not found"

    def test_create_appointment_doctor_not_found(self):
        """Test creating appointment with non-existent doctor."""
        start_time = datetime.now(timezone.utc) + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)

        response = client.post(
            "/appointments",
            json={
                "patient_id": self.patient_id,
                "doctor_id": 9999,
                "appointment_start": start_time.isoformat(),
                "appointment_end": end_time.isoformat()
            }
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Doctor not found"

    def test_get_all_appointments(self):
        """Test retrieving all appointments."""
        # Create an appointment
        start_time = datetime.now(timezone.utc) + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)

        client.post(
            "/appointments",
            json={
                "patient_id": self.patient_id,
                "doctor_id": self.doctor_id,
                "appointment_start": start_time.isoformat(),
                "appointment_end": end_time.isoformat()
            }
        )

        response = client.get("/appointments")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1

    def test_get_all_appointments_empty(self):
        """Test retrieving appointments when none exist."""
        response = client.get("/appointments")

        assert response.status_code == 200
        assert response.json() == []

    def test_get_appointment_by_id(self):
        """Test retrieving an appointment by ID."""
        # Create an appointment
        start_time = datetime.now(timezone.utc) + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)

        create_response = client.post(
            "/appointments",
            json={
                "patient_id": self.patient_id,
                "doctor_id": self.doctor_id,
                "appointment_start": start_time.isoformat(),
                "appointment_end": end_time.isoformat()
            }
        )
        appointment_id = create_response.json()["id"]

        response = client.get(f"/appointments/{appointment_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == appointment_id

    def test_get_appointment_not_found(self):
        """Test retrieving a non-existent appointment."""
        response = client.get("/appointments/9999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Appointment not found"

    def test_overlapping_appointment_full_overlap(self):
        """Test preventing overlapping appointment (complete overlap)."""
        start_time = datetime.now(timezone.utc) + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)

        # Create first appointment
        client.post(
            "/appointments",
            json={
                "patient_id": self.patient_id,
                "doctor_id": self.doctor_id,
                "appointment_start": start_time.isoformat(),
                "appointment_end": end_time.isoformat()
            }
        )

        # Try to create overlapping appointment
        response = client.post(
            "/appointments",
            json={
                "patient_id": self.patient_id,
                "doctor_id": self.doctor_id,
                "appointment_start": start_time.isoformat(),
                "appointment_end": end_time.isoformat()
            }
        )

        assert response.status_code == 400
        assert "overlaps" in response.json()["detail"]

    def test_overlapping_appointment_partial_overlap(self):
        """Test preventing partially overlapping appointment."""
        start_time = datetime.now(timezone.utc) + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)

        # Create first appointment: 10:00 - 11:00
        client.post(
            "/appointments",
            json={
                "patient_id": self.patient_id,
                "doctor_id": self.doctor_id,
                "appointment_start": start_time.isoformat(),
                "appointment_end": end_time.isoformat()
            }
        )

        # Try to create overlapping appointment: 10:30 - 11:30
        overlap_start = start_time + timedelta(minutes=30)
        overlap_end = end_time + timedelta(minutes=30)

        response = client.post(
            "/appointments",
            json={
                "patient_id": self.patient_id,
                "doctor_id": self.doctor_id,
                "appointment_start": overlap_start.isoformat(),
                "appointment_end": overlap_end.isoformat()
            }
        )

        assert response.status_code == 400
        assert "overlaps" in response.json()["detail"]

    def test_adjacent_appointment_allowed(self):
        """Test that adjacent appointments are allowed."""
        start_time = datetime.now(timezone.utc) + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)

        # Create first appointment: 10:00 - 11:00
        client.post(
            "/appointments",
            json={
                "patient_id": self.patient_id,
                "doctor_id": self.doctor_id,
                "appointment_start": start_time.isoformat(),
                "appointment_end": end_time.isoformat()
            }
        )

        # Create adjacent appointment: 11:00 - 12:00
        adjacent_start = end_time
        adjacent_end = end_time + timedelta(hours=1)

        response = client.post(
            "/appointments",
            json={
                "patient_id": self.patient_id,
                "doctor_id": self.doctor_id,
                "appointment_start": adjacent_start.isoformat(),
                "appointment_end": adjacent_end.isoformat()
            }
        )

        assert response.status_code == 201

    def test_overlapping_appointment_different_doctor_allowed(self):
        """Test that overlapping appointments with different doctors are allowed."""
        # Create another doctor
        doctor_response = client.post(
            "/doctors",
            json={
                "name": "Dr. Johnson",
                "specialization": "Neurology"
            }
        )
        doctor_id_2 = doctor_response.json()["id"]

        start_time = datetime.now(timezone.utc) + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)

        # Create appointment with first doctor
        client.post(
            "/appointments",
            json={
                "patient_id": self.patient_id,
                "doctor_id": self.doctor_id,
                "appointment_start": start_time.isoformat(),
                "appointment_end": end_time.isoformat()
            }
        )

        # Create overlapping appointment with different doctor
        response = client.post(
            "/appointments",
            json={
                "patient_id": self.patient_id,
                "doctor_id": doctor_id_2,
                "appointment_start": start_time.isoformat(),
                "appointment_end": end_time.isoformat()
            }
        )

        assert response.status_code == 201


class TestRootEndpoint:
    """Test suite for root endpoint."""

    def test_root_endpoint(self):
        """Test the root endpoint returns health status."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["status"] == "running"
