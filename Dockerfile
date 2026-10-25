# Use official lightweight Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLCONFIGDIR=/tmp/matplotlib \
    SERVER_HOST=0.0.0.0 \
    SERVER_PORT=8050 \
    BIANOR_BACKEND=local \
    BIANOR_LOCAL_CATALOG_ROOT=/app/bianor_local_catalog \
    CACHE_DIR=/app/.bianor_cache

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Ensure cache and temporary directories exist
RUN mkdir -p /app/.bianor_cache /tmp/matplotlib

# Expose default application port
EXPOSE 8050

# Health check to ensure the application is responsive
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8050/ || exit 1

# Launch the Dash application
CMD ["python", "app.py"]
