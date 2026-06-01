SHELL := /bin/bash

VENV := .venv
ACTIVATE := $(VENV)/bin/activate
PYTHON := $(VENV)/bin/python
HOST ?= 127.0.0.1
PORT ?= 8000

.PHONY: help init venv deps check db run shell

help:
	@echo "Available commands:"
	@echo "  make init   - create venv, install/check deps, init db and run app"
	@echo "  make deps   - install dependencies"
	@echo "  make check  - check installed dependencies and Python files"
	@echo "  make db     - initialize SQLite database"
	@echo "  make run    - run FastAPI app"
	@echo "  make shell  - open bash with activated venv"

init: deps check db

venv:
	@test -x "$(PYTHON)" || python3 -m venv "$(VENV)"

deps: venv
	@source "$(ACTIVATE)" && python -m pip install -r requirements.txt
	@source "$(ACTIVATE)" && python -m pip check

check: venv
	@source "$(ACTIVATE)" && python -c "import fastapi, jinja2, uvicorn; print('Dependencies are installed')"
	@source "$(ACTIVATE)" && python -m compileall app scripts

db: venv
	@source "$(ACTIVATE)" && python scripts/init_db.py

run: venv
	@source "$(ACTIVATE)" && uvicorn app.main:app --reload --host "$(HOST)" --port "$(PORT)"

shell: venv
	@bash -c 'source "$(ACTIVATE)" && exec bash'

