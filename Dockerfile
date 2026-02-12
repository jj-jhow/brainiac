FROM python:3.12-slim

# Install system dependencies for build (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy configuration first to leverage Docker cache
COPY pyproject.toml .

# Fix: Copy the src directory (and README if needed) before installing the package.
# pip needs the source code to build the wheel or egg_info.
COPY src/ src/

RUN pip install --no-cache-dir .

# Fix: Set PYTHONPATH so python can resolve imports starting with "src."
ENV PYTHONPATH=/app

# MCP communicate via stdio
CMD ["python", "src/server.py"]