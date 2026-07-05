# Contributing to Qwen Dev Tutor IT

Thank you for considering contributing! This project aims to bring Qwen into Italian developer education, and every contribution helps.

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold it.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/dcargnino/qwen-dev-tutor-it/issues).
2. If not, open a new issue with:
   - A clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, Qwen model/endpoint)

### Suggesting Features

Open an issue with:
- What problem the feature solves
- How it would work (rough sketch is fine)
- Why it fits the project vision

### Pull Requests

1. Fork the repository.
2. Create a branch: `git checkout -b feature/your-feature-name`.
3. Write tests first (TDD — see below).
4. Implement your changes.
5. Run the full test suite: `make test`.
6. Run linting: `make lint`.
7. Commit with a descriptive message.
8. Push and open a PR against `main`.

## Development Setup

```bash
uv venv --python 3.12
uv pip install -e ".[dev]"
cp .env.example .env
# Edit .env with your API key
```

## Testing Guidelines

- **Test-first (TDD)**: write the failing test before the implementation.
- **Coverage**: every new module needs corresponding tests in `tests/`.
- **Run tests**: `make test` or `.venv/bin/python -m pytest tests/ -v`.
- **No regressions**: the full suite must pass before committing.

## Linting

We use [ruff](https://docs.astral.sh/ruff/) for linting:

```bash
make lint        # check
make lint-fix    # auto-fix
```

## Commit Messages

Use conventional commits:

```
feat: add vision analysis endpoint
fix: handle empty API key for local models
docs: update README with configuration examples
test: add streaming endpoint tests
```

## Project Structure

```
src/qwen_dev_tutor/    # Source code
tests/                 # Test files
exercises/             # Workshop exercises
config/                # Example configuration files
```
