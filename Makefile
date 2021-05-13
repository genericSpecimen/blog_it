VENV := env
BIN := $(VENV)/bin
PYTHON := $(BIN)/python3
SHELL := /bin/bash
.PHONY: venv
venv:
	python3 -m venv $(VENV) && source $(BIN)/activate

.PHONY: install
install: venv
	$(BIN)/pip install --upgrade -r requirements.txt

freeze:
	$(BIN)/pip freeze > requirements.txt

migrate:
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate

collectstatic:
	$(PYTHON) manage.py collectstatic

.PHONY: test
test:
	$(PYTHON) manage.py test

.PHONY: coverage
coverage:
	$(PYTHON) -m coverage erase
	$(PYTHON) -m coverage run --source='.' --omit='*/$(VENV)/*' --branch manage.py test
	$(PYTHON) -m coverage report --fail-under=90 --show-missing --skip-covered

.PHONY: run
run:
	$(PYTHON) manage.py runserver

start: install migrate collectstatic run
