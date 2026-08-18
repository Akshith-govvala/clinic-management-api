# Clinic Management API

Hospital Appointment Management System using FastAPI, SQLAlchemy, and PostgreSQL.

## Overview

A comprehensive REST API for managing hospital appointments with patient and doctor scheduling. Built with modern Python web frameworks and best practices for clean architecture.

## Features

- ✅ FastAPI REST API with automatic documentation (Swagger UI)
- ✅ SQLAlchemy ORM with SQLite database
- ✅ Pydantic data validation
- ✅ Appointment overlap prevention for doctors
- ✅ Database migrations with Alembic
- ✅ Comprehensive test suite with 85%+ coverage
- ✅ Docker containerization
- ✅ GitHub Actions CI/CD pipeline
- ✅ Automated security scanning with Bandit
- ✅ Code quality checking with Ruff

## Project Structure

```
clinic-management-api/
├── src/
│   └── clinic_api/
│       ├── __init__.py
│       ├── main.py
│       ├── database.py
│       ├── models/
│       │   ├── patient.py
│       │   ├── doctor.py
│       │   └── appointment.py
│       ├── schemas/
│       │   ├── patient.py
│       │   ├── doctor.py
│       │   └── appointment.py
│       ├── routers/
│       │   ├── patient.py
│       │   ├── doctor.py
│       │   └── appointment.py
│       └── services/
│           ├── patient_service.py
│           ├── doctor_service.py
│           └── appointment_service.py
├── tests/
│   ├── conftest.py
│   └── test_api.py
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── .github/
│   └── workflows/
│       └── ci.yml
├── pyproject.toml
├── alembic.ini
├── Dockerfile
├── .gitignore
├── .dockerignore
└── README.md
```

## Technology Stack

- **Python 3.10+**
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **Pytest** - Testing framework
- **Ruff** - Code linter
- **Bandit** - Security analyzer
- **Docker** - Containerization
- **GitHub Actions** - CI/CD

## Installation

### Prerequisites
- Python 3.10+
- pip or uv

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd clinic-management-api
```

2. Install dependencies:
```bash
pip install -e .
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the development server:
```bash
uvicorn clinic_api.main:app --reload --app-dir src
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Patients
- `GET /patients` - Retrieve all patients
- `POST /patients` - Create a new patient
- `GET /patients/{id}` - Retrieve patient by ID

### Doctors
- `GET /doctors` - Retrieve all doctors
- `POST /doctors` - Create a new doctor
- `GET /doctors/{id}` - Retrieve doctor by ID

### Appointments
- `GET /appointments` - Retrieve all appointments
- `POST /appointments` - Create a new appointment
- `GET /appointments/{id}` - Retrieve appointment by ID

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Database Models

### Patient
- id (Primary Key)
- name (String)
- email (String, Unique)
- phone (String)

### Doctor
- id (Primary Key)
- name (String)
- specialization (String)

### Appointment
- id (Primary Key)
- patient_id (Foreign Key → Patient)
- doctor_id (Foreign Key → Doctor)
- appointment_start (DateTime)
- appointment_end (DateTime)

## Business Rules

1. Appointment end time must be after start time
2. Patient and doctor must exist before creating an appointment
3. **Overlapping appointments are prevented**: A doctor cannot have overlapping appointments
   - Condition: `existing_start < new_end AND existing_end > new_start`

## Testing

Run the test suite:
```bash
pytest
```

Run tests with coverage report:
```bash
pytest --cov=src/clinic_api --cov-report=html
```

Coverage should be at least 85%.

## Code Quality

### Linting
```bash
ruff check src tests
```

### Security Analysis
```bash
bandit -r src
```

## Docker

### Build the Docker image:
```bash
docker build -t clinic-management-api:latest .
```

### Run the container:
```bash
docker run -p 8000:8000 clinic-management-api:latest
```

## CI/CD Pipeline

The GitHub Actions workflow automatically:
1. **Linting** - Validates code quality with Ruff
2. **Testing** - Runs tests with 85% coverage requirement
3. **Security** - Scans code with Bandit
4. **Build** - Builds Docker image
5. **Publish** - Pushes image to Docker Hub (on main branch)

### Secrets Required

Set these secrets in GitHub repository settings for Docker Hub publishing:
- `DOCKER_HUB_USERNAME` - Your Docker Hub username
- `DOCKER_HUB_ACCESS_TOKEN` - Docker Hub access token

## Example Requests

### Create Patient
```bash
curl -X POST "http://localhost:8000/patients" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "phone": "1234567890"}'
```

### Create Doctor
```bash
curl -X POST "http://localhost:8000/doctors" \
  -H "Content-Type: application/json" \
  -d '{"name": "Dr. Smith", "specialization": "Cardiology"}'
```

### Create Appointment
```bash
curl -X POST "http://localhost:8000/appointments" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "doctor_id": 1,
    "appointment_start": "2026-08-19T10:00:00",
    "appointment_end": "2026-08-19T11:00:00"
  }'
```

## Error Handling

The API returns appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error, overlapping appointment)
- `404` - Not Found
- `422` - Unprocessable Entity (validation error)

## Development

### Create a new migration
```bash
alembic revision --autogenerate -m "Description"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migration
```bash
alembic downgrade -1
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Ensure tests pass and coverage is maintained
4. Submit a pull request

## License

MIT License

## Support

For issues and questions, please create an issue in the repository.
