"""Configuration and credential management for AI Pioneers cloud."""

from __future__ import annotations

import json
from pathlib import Path
from pydantic import BaseModel


PIONEERS_DIR = Path.home() / ".pioneers"
CREDENTIALS_FILE = PIONEERS_DIR / "credentials.json"
CONFIG_FILE = PIONEERS_DIR / "config.json"

API_BASE_URL = "https://api.pioneers.ai"
AUTH_URL = "https://app.pioneers.ai/auth/github"


class Credentials(BaseModel):
    """Stored authentication credentials."""

    access_token: str
    username: str
    email: str | None = None
    plan: str = "free"


class PioneersConfig(BaseModel):
    """Local configuration for cloud features."""

    backend: str = "local"  # "local" or "cloud"
    api_url: str = API_BASE_URL


def ensure_dir() -> Path:
    """Ensure ~/.pioneers/ directory exists."""
    PIONEERS_DIR.mkdir(parents=True, exist_ok=True)
    return PIONEERS_DIR


def load_credentials() -> Credentials | None:
    """Load stored credentials, or None if not logged in."""
    if not CREDENTIALS_FILE.exists():
        return None
    try:
        data = json.loads(CREDENTIALS_FILE.read_text(encoding="utf-8"))
        return Credentials(**data)
    except (json.JSONDecodeError, ValueError):
        return None


def save_credentials(creds: Credentials) -> None:
    """Save credentials to disk."""
    ensure_dir()
    CREDENTIALS_FILE.write_text(
        creds.model_dump_json(indent=2),
        encoding="utf-8",
    )
    CREDENTIALS_FILE.chmod(0o600)


def delete_credentials() -> bool:
    """Delete stored credentials. Returns True if they existed."""
    if CREDENTIALS_FILE.exists():
        CREDENTIALS_FILE.unlink()
        return True
    return False


def load_config() -> PioneersConfig:
    """Load local config, or return defaults."""
    if not CONFIG_FILE.exists():
        return PioneersConfig()
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        return PioneersConfig(**data)
    except (json.JSONDecodeError, ValueError):
        return PioneersConfig()


def save_config(config: PioneersConfig) -> None:
    """Save config to disk."""
    ensure_dir()
    CONFIG_FILE.write_text(
        config.model_dump_json(indent=2),
        encoding="utf-8",
    )
