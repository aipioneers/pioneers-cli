# pioneers-cli

Connect your tools to the AI Pioneers cloud.

[![PyPI](https://img.shields.io/pypi/v/pioneers-cli)](https://pypi.org/project/pioneers-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)

The authentication and configuration layer for [AI Pioneers](https://pioneers.ai) cloud features. Connects your local CLI tools (code-explore, code-adapt) to the optional cloud backend via GitHub OAuth.

## Quick Start

```bash
pip install pioneers-cli
```

```bash
# Authenticate via GitHub
pioneers login

# Check status
pioneers status

# Enable cloud backend for code-explore / code-adapt
pioneers config backend cloud

# Switch back to local
pioneers config backend local

# Log out
pioneers logout
```

## Commands

| Command | Description |
|---------|-------------|
| `pioneers login` | Authenticate via GitHub OAuth device flow |
| `pioneers logout` | Remove stored credentials |
| `pioneers status` | Show current user, plan, and backend setting |
| `pioneers config backend <local\|cloud>` | Switch between local and cloud mode |

## Privacy

Your source code never leaves your machine. The cloud backend only stores project metadata — names, languages, dependencies, patterns, and summaries. All analysis and indexing happens locally.

## For Tool Authors

Other CLIs can check authentication status programmatically:

```python
from pioneers_cli.config import load_credentials, load_config

creds = load_credentials()
if creds:
    print(f"Logged in as {creds.username}")

config = load_config()
if config.backend == "cloud":
    print(f"Using cloud API at {config.api_url}")
```

Credentials are stored in `~/.pioneers/credentials.json`.

## Development

```bash
git clone https://github.com/aipioneers/pioneers-cli.git
cd pioneers-cli
pip install -e ".[dev]"
pytest tests/ -v
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

[MIT](LICENSE)

---

Part of the [AI Pioneers](https://pioneers.ai) ecosystem · [code-explore](https://github.com/aipioneers/code-explore) · [code-adapt](https://github.com/aipioneers/code-adapt) · [spec-intelligence](https://github.com/aipioneers/spec-intelligence)
