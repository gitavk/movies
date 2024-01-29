include .env

fmt_cmd = ruff format 
lint_cmd = ruff check 
dc = docker-compose

lint-local:
	$(fmt_cmd) src --check --no-cache
	$(lint_cmd) src --no-cache

fix-local:
	$(fmt_cmd) src --no-cache
	$(fmt_cmd) tests --no-cache
	$(lint_cmd) src --fix --no-cache
	$(lint_cmd) tests --fix --no-cache

up-local:
	python -m uvicorn src.main:app --reload

build-app:
	$(dc) build

build-test:
	$(dc) -f compose.test.yml build

build-all: build-app build-test

up-app:
	$(dc) up -d

db-shell:
	$(dc) exec apidb psql -h localhost -U $(POSTGRES_USER) -d $(POSTGRES_DB)

run-tests:
	$(dc) -f compose.test.yml up --abort-on-container-exit

purge-app:
	$(dc) down -v --rmi all

purge-tests:
	$(dc) -f compose.test.yml down -v --rmi all

purge-all: purge-app purge-test
