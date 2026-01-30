# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN pip install --no-cache-dir build

# Copy backend dependency files
COPY backend/pyproject.toml ./

# Install dependencies
RUN pip install --no-cache-dir .

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application source
COPY backend/app ./app

# Environment variables for Neo4j connection (override at runtime)
ENV NEO4J_URL=bolt://host.docker.internal:7687
ENV NEO4J_USER=neo4j
ENV NEO4J_PASSWORD=

# Expose the API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
