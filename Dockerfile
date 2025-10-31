# Use official Python image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Exclude virtual environment and cache folders via .dockerignore

# Set default entrypoint (adjust as needed)
ENTRYPOINT [ "python", "-m", "canopy.main" ] 