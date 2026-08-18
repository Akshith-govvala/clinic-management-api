"""Test to verify dependency override is working."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import clinic_api.database as db_module
from clinic_api.database import get_db

print("Step 1: get_db function:", get_db)
print("Step 2: db_module.get_db function:", db_module.get_db)
print("Step 3: Are they the same?", get_db is db_module.get_db)

# Now check conftest's get_db
from tests.conftest import get_db as conftest_get_db

print("Step 4: conftest's get_db:", conftest_get_db)
print("Step 5: Is conftest's get_db the same as original?", conftest_get_db is get_db)

# Check the app's dependency overrides
from tests.conftest import app

print("Step 6: app.dependency_overrides:", app.dependency_overrides)
print("Step 7: Keys in overrides:", list(app.dependency_overrides.keys()))
print("Step 8: get_db in overrides?", get_db in app.dependency_overrides)
