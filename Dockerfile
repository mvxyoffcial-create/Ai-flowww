FROM python:3.10-slim

WORKDIR /app

# Install only essential system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .
COPY templates/ templates/
RUN mkdir -p static

# Environment
ENV PORT=8000
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Run with minimal resources
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "1", "--timeout", "300", "--worker-class", "sync", "--max-requests", "100", "--max-requests-jitter", "10", "app:app"]
