FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -e .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "clinic_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]
