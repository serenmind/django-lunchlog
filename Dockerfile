# Development Dockerfile for lunchlog
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

# Install system dependencies required for building some Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       gcc \
       curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (official installer)
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

# Copy only dependency files and README first to leverage Docker layer cache
# Poetry expects the path specified in pyproject.toml `readme` to exist when installing the project.
COPY pyproject.toml poetry.lock* README.md /app/

# Install Python dependencies into the container Python environment (skip installing the project)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the project
COPY . /app

# Add entrypoint and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

# Use entrypoint to run migrations and optional setup, then run CMD
ENTRYPOINT ["/entrypoint.sh"]
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
