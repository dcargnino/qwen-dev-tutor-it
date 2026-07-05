.PHONY: install test lint run docker-build docker-run clean

install:
	uv venv --python 3.12
	uv pip install -e ".[dev]"

test:
	.venv/bin/python -m pytest tests/ -v

test-quick:
	.venv/bin/python -m pytest tests/ -q

lint:
	.venv/bin/ruff check src/qwen_dev_tutor/ tests/

lint-fix:
	.venv/bin/ruff check --fix src/qwen_dev_tutor/ tests/

run:
	.venv/bin/uvicorn qwen_dev_tutor.api:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker compose build

docker-run:
	docker compose up -d

docker-stop:
	docker compose down

docker-logs:
	docker compose logs -f

demo:
	bash exercises/demo.sh

clean:
	rm -rf .venv/ .pytest_cache/ __pycache__/
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
