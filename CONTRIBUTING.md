# Contributing to pioneers-cli

Contributions are welcome. Whether it's a bug report, feature suggestion, or pull request — thank you for helping improve pioneers-cli.

## Reporting Bugs

Open an issue using the **Bug Report** template. Include steps to reproduce, expected behavior, and your environment.

## Suggesting Features

Open an issue using the **Feature Request** template. Describe the use case and why it matters.

## Development Setup

```bash
git clone https://github.com/aipioneers/pioneers-cli.git
cd pioneers-cli
pip install -e ".[dev]"
pytest tests/ -v
```

Requires Python 3.11+.

## Pull Requests

1. Fork the repo and create a branch from `main`
2. Write tests for new functionality
3. Run `pytest tests/ -v` and make sure everything passes
4. Open a PR with a clear description of what and why

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). Be kind.
