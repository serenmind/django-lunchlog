# LunchLog

Backend Django REST API for managing office lunch receipts and restaurant recommendations.


Quick start (local development with Docker):

1. Copy `.env.example` is present in the project root to `.env` file and add appropriate environment variables as needed.

2. Start development services (Postgres, Redis, web, worker):

```bash
make build-up
```

3. Run tests:

```bash
make test
```

Configuration notes:
- Set AWS S3 credentials in `.env.dev` and update `DEFAULT_FILE_STORAGE` in `config/settings.py` to enable uploads to S3.
- Set `GOOGLE_PLACES_API_KEY` in `.env.dev` for the Celery task to fetch place details.
- Celery worker runs in the `worker` service and expects Redis at `redis:6379`.

Endpoints:
- POST /auth/signup/
- POST /auth/login/
- /receipts/ (CRUD)
- GET /recommendations/?location=<city>
