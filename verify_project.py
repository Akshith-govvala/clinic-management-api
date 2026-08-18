#!/usr/bin/env python
"""Quick test to verify project setup."""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Test imports
try:
    from clinic_api.main import app
    from clinic_api.models.patient import Patient
    from clinic_api.models.doctor import Doctor
    from clinic_api.models.appointment import Appointment
    from clinic_api.database import Base, engine
    print("✓ All imports successful")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

# Test database setup
try:
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")
except Exception as e:
    print(f"✗ Database setup error: {e}")
    sys.exit(1)

# Test API
try:
    from fastapi.testclient import TestClient
    client = TestClient(app)
    
    # Test root endpoint
    response = client.get("/")
    assert response.status_code == 200
    print("✓ API root endpoint works")
    
    # Test create patient
    response = client.post(
        "/patients",
        json={
            "name": "Test Patient",
            "email": "test@example.com",
            "phone": "1234567890"
        }
    )
    assert response.status_code == 201
    print("✓ Patient creation works")
    
    # Test get patients
    response = client.get("/patients")
    assert response.status_code == 200
    print("✓ Get patients works")
    
except Exception as e:
    print(f"✗ API test error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓✓✓ All basic tests passed! ✓✓✓")
print("\nNow running full test suite...")

# Run pytest
import subprocess
result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/", "-v", "--cov=src/clinic_api", "--cov-fail-under=85"],
    cwd=str(Path(__file__).parent)
)

sys.exit(result.returncode)
