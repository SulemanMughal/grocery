# Stage 1: Base build stage

# ---- Builder Stage ----
FROM python:3.13-slim AS builder
WORKDIR /app

# Install build dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
  libsqlite3-dev build-essential libpq-dev \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Environment variables for Python optimization
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip and install dependencies
RUN pip install --upgrade pip

# Copy only requirements for better layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage

# ---- Final Stage ----
FROM python:3.13-slim
WORKDIR /app

# Create non-root user
RUN useradd -m -r appuser

# Create directories with proper permissions as root
RUN mkdir -p /data/sqlite /app/logs /app/static /app/staticfiles && \
    chown -R appuser:appuser /data/sqlite /app/logs /app/static /app/staticfiles && \
    chmod -R 755 /data/sqlite /app/logs /app/static /app/staticfiles

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application code and set ownership
COPY . .
RUN chown -R appuser:appuser /app

# Copy and set permissions for entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod 750 /app/entrypoint.sh

# Environment variables for Python optimization
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"

# Switch to non-root user for security
USER appuser

EXPOSE 8000