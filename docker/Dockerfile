# Use slim Python base
FROM python:3.12-slim

# Install system deps (needed for psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -Ls https://astral.sh/uv/install.sh | bash
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy dependency files first (for caching)
COPY pyproject.toml uv.lock* ./

# Install dependencies (no dev deps)
RUN uv sync --no-dev

# Copy project files
COPY . .

# Run app
CMD ["uv", "run", "python", "run.py"]