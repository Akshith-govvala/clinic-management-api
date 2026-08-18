#!/usr/bin/env python
"""Run pytest tests."""
import subprocess
import sys
from pathlib import Path

result = subprocess.run(
    [
        sys.executable,
        "-m",
        "pytest",
        "tests/",
        "-v",
        "--cov=src/clinic_api",
        "--cov-report=term-missing",
        "--cov-fail-under=85",
    ],
    cwd=str(Path(__file__).parent),
    check=False,
)

sys.exit(result.returncode)
