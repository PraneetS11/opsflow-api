.PHONY: install run test lint services stop
install:
	python3.12 -m venv .venv
	.venv/bin/python -m pip install -r requirements.lock
	.venv/bin/python -m pip install --no-deps -e .
run:
	.venv/bin/python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8002
test:
	.venv/bin/python -m pytest -q
lint:
	.venv/bin/ruff check .
	.venv/bin/ruff format --check .
services:
	docker compose up -d --wait
stop:
	docker compose stop
