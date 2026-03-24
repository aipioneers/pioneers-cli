# pioneers-cli

CLI for AI Pioneers cloud — authenticate, configure, and connect your tools.

## Install

```bash
pip install pioneers-cli
```

## Usage

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

## What It Does

`pioneers-cli` is the authentication and configuration layer for [AI Pioneers](https://pioneers.ai) cloud features. It connects your local CLI tools (code-explore, code-adapt) to the optional cloud backend.

- **Login** — GitHub OAuth device flow, stores token in `~/.pioneers/credentials.json`
- **Config** — Switch between `local` and `cloud` backend
- **Status** — Show current user, plan, and backend setting

Your source code never leaves your machine. The cloud only stores project metadata (name, languages, dependencies, patterns, summaries).

## For Tool Authors

Other CLIs can check authentication status:

```python
from pioneers_cli.config import load_credentials, load_config

creds = load_credentials()
if creds:
    print(f"Logged in as {creds.username}")

config = load_config()
if config.backend == "cloud":
    print(f"Using cloud API at {config.api_url}")
```

## License

MIT
