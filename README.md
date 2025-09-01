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

Endpoints:
- POST /auth/signup/
- POST /auth/login/
- /receipts/ (CRUD)
- /receipts/?month=<1-12> (CRUD)
- GET /recommendations/?location=<adress>
