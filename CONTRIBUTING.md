# Contributing to Retro Game Engine

Thank you for your interest in contributing to Retro Game Engine! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/ahmed5145/retro_game_engine.git
cd retro_game_engine
```

2. Install Poetry (dependency management):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies:
```bash
poetry install
```

4. Install pre-commit hooks:
```bash
poetry run pre-commit install
```

## Development Workflow

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and ensure all tests pass:
```bash
poetry run pytest
```

3. Run type checking and linting:
```bash
poetry run mypy src tests
poetry run pylint src tests
```

4. Commit your changes using conventional commits:
```bash
git commit -m "feat: add new feature"
```

5. Push to your fork and create a pull request

## Code Style

- Follow PEP 8 guidelines
- Use type hints for all function arguments and return values
- Write docstrings for all public functions, classes, and modules
- Keep functions focused and small
- Write unit tests for new functionality

## Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src

# Run specific test file
poetry run pytest tests/path/to/test_file.py
```

## Pre-commit Hooks

We use pre-commit hooks to ensure code quality. They run automatically on commit, but you can also run them manually:

```bash
poetry run pre-commit run --all-files
```

## Release Process

1. Update version in pyproject.toml
2. Create and push a new tag:
```bash
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

## Getting Help

- Open an issue for bugs or feature requests
- Join our Discord server for discussions
- Check the documentation for detailed information

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.