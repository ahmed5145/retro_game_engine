# Contributing to Retro Game Engine

First off, thank you for considering contributing to Retro Game Engine! It's people like you that make it such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check [this list](https://github.com/ahmed5145/retro_game_engine/issues) as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include screenshots and animated GIFs if possible

### Suggesting Enhancements

Enhancement suggestions are tracked as [GitHub issues](https://github.com/ahmed5145/retro_game_engine/issues). When creating an enhancement suggestion, please provide:

* A clear and descriptive title
* A detailed description of the proposed feature
* Examples of how the feature would be used
* Explanation of why this enhancement would be useful

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints

## Development Process

1. Clone the repository
```bash
git clone https://github.com/ahmed5145/retro_game_engine.git
cd retro_game_engine
```

2. Install development dependencies
```bash
poetry install
```

3. Create a branch
```bash
git checkout -b feature/my-feature
# or
git checkout -b fix/my-fix
```

4. Make your changes and commit
```bash
git add .
git commit -m "Description of changes"
```

5. Run tests
```bash
poetry run pytest
```

6. Push and create a Pull Request
```bash
git push origin feature/my-feature
```

## Style Guide

We use several tools to maintain code quality:

* **Black** for code formatting
* **isort** for import sorting
* **mypy** for type checking
* **pylint** for code analysis
* **flake8** for style guide enforcement

Run all checks with:
```bash
poetry run pre-commit run --all-files
```

## Documentation

* Use docstrings for all public modules, functions, classes, and methods
* Follow Google style for docstrings
* Keep documentation up to date with code changes
* Add examples for complex functionality

## Testing

* Write unit tests for new features
* Maintain or improve test coverage
* Test edge cases and error conditions
* Use pytest fixtures and parametrize when appropriate

## Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
