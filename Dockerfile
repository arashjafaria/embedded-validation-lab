
# Use Python 3.12 inside the container
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install the testing dependencies
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy our AEB program and tests
COPY aeb.py pyproject.toml ./
COPY tests/ ./tests/

# Run automated tests when the container starts
CMD ["python", "-m", "pytest", "-v"]

