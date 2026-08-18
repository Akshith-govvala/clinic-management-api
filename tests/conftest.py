"""Test configuration and fixtures."""

import sys
from pathlib import Path

# Add src to path so we can import clinic_api
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from clinic_api.database import Base, get_db
from clinic_api.main import app

# Use a test-specific SQLite database file
test_db_path = Path(__file__).parent.parent / "test_clinic.db"
# Delete the test database if it exists to start fresh
if test_db_path.exists():
    test_db_path.unlink()

TEST_SQLALCHEMY_DATABASE_URL = f"sqlite:///{test_db_path}"

test_engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)

# Create all tables in the test database using Base.metadata
Base.metadata.create_all(bind=test_engine)


def override_get_db():
    """Override database dependency for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the get_db dependency
app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    """Reset database before each test."""
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield


@pytest.fixture
def test_patient():
    """Fixture that creates a test patient and returns its ID."""
    response = client.post(
        "/patients",
        json={
            "name": "Test Patient",
            "email": "test@example.com",
            "phone": "1234567890",
        },
    )
    return response.json()["id"]


@pytest.fixture
def test_doctor():
    """Fixture that creates a test doctor and returns its ID."""
    response = client.post(
        "/doctors", json={"name": "Dr. Test", "specialization": "General Practice"}
    )
    return response.json()["id"]
