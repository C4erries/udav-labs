SHELL := /bin/bash

VENV := .venv
ACTIVATE := $(VENV)/bin/activate
PYTHON := $(VENV)/bin/python
HOST ?= 127.0.0.1
PORT ?= 8000

.PHONY: help init venv deps check migrations migrate seed run shell

help:
	@echo "Available commands:"
	@echo "  make init        - create venv, install/check deps, migrate, seed and run app"
	@echo "  make deps        - install dependencies"
	@echo "  make check       - run Django checks"
	@echo "  make migrations  - create migrations"
	@echo "  make migrate     - apply migrations"
	@echo "  make seed        - load demo data"
	@echo "  make run         - run Django dev server"
	@echo "  make shell       - open bash with activated venv"

init: deps check migrate seed

venv:
	@test -x "$(PYTHON)" || python3 -m venv "$(VENV)"

deps: venv
	@source "$(ACTIVATE)" && python -m pip install -r requirements.txt
	@source "$(ACTIVATE)" && python -m pip check

check: venv
	@source "$(ACTIVATE)" && python -c "import django; print('Django', django.get_version())"
	@source "$(ACTIVATE)" && python manage.py check

migrations: venv
	@source "$(ACTIVATE)" && python manage.py makemigrations

migrate: venv
	@source "$(ACTIVATE)" && python manage.py migrate

seed: venv
	@source "$(ACTIVATE)" && python manage.py seed_demo

admin: venv
	export DJANGO_SUPERUSER_USERNAME=admin
	export DJANGO_SUPERUSER_EMAIL=admin@example.ru
	export DJANGO_SUPERUSER_PASSWORD=1234
	@source "$(ACTIVATE)" && python manage.py createsuperuser --noinput

run: venv
	@source "$(ACTIVATE)" && python manage.py runserver "$(HOST):$(PORT)"

shell: venv
	@bash -c 'source "$(ACTIVATE)" && exec bash'

