# LunchLog

Backend Django REST API for managing office lunch receipts and restaurant recommendations.

---

## Overview

This repository provides a Django + DRF backend with:
- Receipt CRUD and image uploads (S3 via django-storages)
- Celery worker for background tasks (recommendations)
- PostgreSQL database and Redis broker (via Docker Compose)

---

## Prerequisites

- Docker & Docker Compose (v2) installed and working
- Poetry (for local development without Docker)
- AWS credentials if you use S3 (set in `.env`, see below)

---

## Initial setup

1. Copy the example env file and edit:
   ```bash
   cp .env.example .env
   # Edit .env and provide DB, Redis and AWS credentials
   ```

2. (Optional) Install dependencies locally (if you want to run without Docker):
   ```bash
   poetry install
   ```

Notes:
- `.env` is listed in `.gitignore`. Do not commit secrets.
- Required env vars include database, Redis, and (if using S3) `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`, `AWS_S3_REGION_NAME`.

---

## Run (development with Docker)

Start services (Postgres, Redis, web, celery-worker):

- Build + start (recommended first run):
  ```bash
  make build-up
  # or
  docker compose up --build
  ```

- Start (no build):
  ```bash
  make up
  # or
  docker compose up
  ```

- Start services in background:
  ```bash
  docker compose up -d
  ```

Useful targets (from Makefile):

- Run migrations:
  ```bash
  make migrate
  ```

- Run makemigrations:
  ```bash
  make makemigrations a=<app_name>
  ```

- Create superuser:
  ```bash
  make createsuperuser
  ```

- Collect static files:
  ```bash
  make collectstatic
  ```

- Open a shell inside the web container:
  ```bash
  make shell
  # or
  docker compose exec web /bin/sh
  ```

The web service will be available at: http://0.0.0.0:8000

---

## Running Celery worker

The `celery-worker` service is defined in `docker-compose.yml`. When you run `docker compose up` it will be started as configured. Logs are available with:
```bash
docker compose logs -f celery-worker
```

---

## Tests

Tests are executed inside the `web` container (so they can reach the Docker Postgres service).

- Run tests in an already-running `web` container (no build):
  ```bash
  make test
  # which executes:
  # docker compose exec web poetry run pytest
  ```

- Build image and run tests (if you want to ensure image has test deps):
  ```bash
  make build
  docker compose run --rm web poetry run pytest
  ```

Notes:
- Tests use `pytest` and `pytest-django`. These are included in the project's `pyproject.toml` so the Docker dev image has them installed during build.
- Some tests mock external calls (S3 / Google Places) so they run offline.

---

## Local development (without Docker)

1. Ensure PostgreSQL and Redis are running on your machine or adjust `DATABASES`/broker settings in `.env`.
2. Install deps:
   ```bash
   poetry install
   ```
3. Run migrations and start the server:
   ```bash
   poetry run python manage.py migrate
   poetry run python manage.py runserver
   ```

---

## Important notes & troubleshooting

- If GitHub blocks pushes due to secret scanning, revoke the leaked keys immediately and remove secrets from commit history before pushing. Do not push `.env` or secrets.
- To generate presigned S3 URLs the app uses django-storages / boto3. If you removed custom domain settings, signed URLs will use S3 endpoints.
- The entrypoint script runs migrations/collectstatic only when needed (it uses Django checks), so container restarts are faster.

---

## Endpoints (quick)

- POST /auth/signup/ — register
- POST /auth/login/ — login (DRF browsable)
- POST /auth/logout/ — logout (DRF browsable)
- /receipts/ — Receipt CRUD (upload-images action available on detail)
- /recommendations/ — get recommended places
