# Makefile - common development tasks for lunchlog

.PHONY: install lock add migrate makemigrations createsuperuser collectstatic test test-run test-exec build up build-up down shell recreate

install:
	poetry install

lock:
	poetry lock

add:
	@if [ -z "$(p)" ]; then echo "Specify package with p=<pkg>"; exit 1; fi
	poetry add $(p)

migrate:
	docker compose exec web poetry run python manage.py migrate

makemigrations:
	docker compose exec web poetry run python manage.py makemigrations $(a)

createsuperuser:
	docker compose exec web poetry run python manage.py createsuperuser

collectstatic:
	docker compose exec web poetry run python manage.py collectstatic --noinput

# Run tests inside an already-running web container. This will fail if web is not running.
test:
	docker compose exec web poetry run pytest

# Docker-related targets
build:
	docker compose build --pull

up:
	# start services (foreground)
	docker compose up

build-up:
	# build and start services
	docker compose up --build

down:
	# stop and remove services
	docker compose down

shell:
	docker compose exec web /bin/sh

recreate: down build up
