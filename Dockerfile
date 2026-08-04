# Multi-stage Docker build for Quantum Project 2
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY requirements.txt .
COPY requirements-dev.txt .
COPY setup.py .
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r requirements-dev.txt

# Production stage
FROM python:3.11-slim as production

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    USER=quantum \
    UID=1000 \
    GID=1000

# Create non-root user
RUN groupadd -g $GID $USER && \
    useradd -u $UID -g $GID -m $USER

# Set work directory
WORKDIR /app

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from base stage
COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

# Copy project files
COPY --chown=$USER:$USER . .

# Switch to non-root user
USER $USER

# Expose port for potential web services
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from deutsch_jozsa import DeutschJozsaAlgorithm; print('OK')" || exit 1

# Default command
CMD ["python", "deutsch_jozsa.py"]