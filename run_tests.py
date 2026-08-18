#!/usr/bin/env python
"""Run tests with coverage."""

import sys
import subprocess

result = subprocess.run(
    [
        sys.executable,
        "-m",
        "pytest",
        "tests/",
        "--cov=src/clinic_api",
        "--cov-report=term-missing",
        "--cov-report=html",
        "-v"
    ],
    cwd="c:\\Users\\Admin\\clinic-management-api"
)

sys.exit(result.returncode)
