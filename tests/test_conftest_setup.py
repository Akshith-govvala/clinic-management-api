"""Simple test to verify conftest database setup."""

from tests.conftest import client, test_engine, Base


def test_database_setup():
    """Verify that the test database is set up correctly."""
    # Check that Base.metadata has tables
    assert "patients" in Base.metadata.tables
    assert "doctors" in Base.metadata.tables
    assert "appointments" in Base.metadata.tables
    
    # Check that tables exist in the test database
    from sqlalchemy import inspect, text
    inspector = inspect(test_engine)
    tables = inspector.get_table_names()
    assert "patients" in tables
    assert "doctors" in tables
    assert "appointments" in tables
    
    # Verify we can query the tables (they should be empty)
    with test_engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM patients"))
        count = result.scalar()
        assert count == 0
