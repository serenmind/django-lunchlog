#!/usr/bin/env sh
# entrypoint.sh - minimal DB-only setup for Docker
set -eu

POETRY=${POETRY:-poetry}
HOST=${POSTGRES_HOST:-db}
PORT=${POSTGRES_PORT:-5432}

echo "[entrypoint] waiting for database ${HOST}:${PORT}..."
python - <<'PY' || exit 1
import socket, time, os, sys
host=os.getenv('POSTGRES_HOST','db')
port=int(os.getenv('POSTGRES_PORT','5432'))
timeout=int(os.getenv('DB_WAIT_SECONDS','60'))
for i in range(timeout):
    try:
        s=socket.create_connection((host,port),2)
        s.close()
        print('database available')
        sys.exit(0)
    except Exception:
        time.sleep(1)
print('Timed out waiting for Postgres', file=sys.stderr)
sys.exit(1)
PY

echo "[entrypoint] running migrations..."
${POETRY} run python manage.py migrate --noinput

echo "[entrypoint] collecting static files..."
${POETRY} run python manage.py collectstatic --noinput

echo "[entrypoint] database setup complete, executing: $@"
exec "$@"
