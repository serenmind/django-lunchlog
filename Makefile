# Makefile - common development tasks for lunchlog

DOCKER_COMPOSE ?= docker compose
POETRY ?= poetry

.PHONY: install lock add migrate makemigrations createsuperuser collectstatic test build up build-up down shell recreate

install:
	$(POETRY) install

lock:
	$(POETRY) lock

add:
	@if [ -z "$(p)" ]; then echo "Specify package with p=<pkg>"; exit 1; fi
	$(POETRY) add $(p)

migrate:
	$(POETRY) run python manage.py migrate

makemigrations:
	$(POETRY) run python manage.py makemigrations $(a)

createsuperuser:
	$(POETRY) run python manage.py createsuperuser

collectstatic:
	$(POETRY) run python manage.py collectstatic --noinput

test:
	$(POETRY) run pytest

# Docker-related targets
build:
	$(DOCKER_COMPOSE) build --pull

up:
	$(DOCKER_COMPOSE) up

build-up:
	$(DOCKER_COMPOSE) up --build

down:
	$(DOCKER_COMPOSE) down

shell:
	$(DOCKER_COMPOSE) exec web /bin/sh

recreate: down build up
