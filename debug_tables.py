#!/usr/bin/env python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from clinic_api.database import Base

print("After importing database, Base tables:", list(Base.metadata.tables.keys()))

print("After importing main, Base tables:", list(Base.metadata.tables.keys()))

from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
print("Before create_all, Base.metadata has:", list(Base.metadata.tables.keys()))
Base.metadata.create_all(bind=engine)
print("After create_all")

# Query the engine to see what tables exist
with engine.connect() as conn:
    result = conn.execute(text('SELECT name FROM sqlite_master WHERE type="table"'))
    tables = [row[0] for row in result]
    print("Tables in engine:", tables)
