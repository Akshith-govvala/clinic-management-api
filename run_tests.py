#!/usr/bin/env python
"""Run tests with coverage."""
#ruff: noqa
import subprocess
import sys

result = subprocess.run(
    [
        sys.executable,
        "-m",
        "pytest",
        "tests/",
        "--cov=src/clinic_api",
        "--cov-report=term-missing",
        "--cov-report=html",
        "-v",
    ],
    cwd="c:\\Users\\Admin\\clinic-management-api",
)

sys.exit(result.returncode)
