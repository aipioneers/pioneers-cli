"""Tests for configuration and credential management."""

import json
from pathlib import Path

from pioneers_cli.config import (
    Credentials,
    PioneersConfig,
    save_credentials,
    load_credentials,
    delete_credentials,
    save_config,
    load_config,
)


def test_credentials_roundtrip(tmp_path, monkeypatch):
    creds_file = tmp_path / "credentials.json"
    monkeypatch.setattr("pioneers_cli.config.CREDENTIALS_FILE", creds_file)
    monkeypatch.setattr("pioneers_cli.config.PIONEERS_DIR", tmp_path)

    creds = Credentials(access_token="ghp_test123", username="testuser", email="test@example.com")
    save_credentials(creds)

    loaded = load_credentials()
    assert loaded is not None
    assert loaded.username == "testuser"
    assert loaded.access_token == "ghp_test123"
    assert loaded.email == "test@example.com"
    assert loaded.plan == "free"


def test_load_credentials_missing(tmp_path, monkeypatch):
    monkeypatch.setattr("pioneers_cli.config.CREDENTIALS_FILE", tmp_path / "nonexistent.json")
    assert load_credentials() is None


def test_delete_credentials(tmp_path, monkeypatch):
    creds_file = tmp_path / "credentials.json"
    monkeypatch.setattr("pioneers_cli.config.CREDENTIALS_FILE", creds_file)
    monkeypatch.setattr("pioneers_cli.config.PIONEERS_DIR", tmp_path)

    creds = Credentials(access_token="ghp_test", username="user")
    save_credentials(creds)
    assert creds_file.exists()

    assert delete_credentials() is True
    assert not creds_file.exists()
    assert delete_credentials() is False


def test_config_defaults():
    config = PioneersConfig()
    assert config.backend == "local"
    assert "pioneers.ai" in config.api_url


def test_config_roundtrip(tmp_path, monkeypatch):
    config_file = tmp_path / "config.json"
    monkeypatch.setattr("pioneers_cli.config.CONFIG_FILE", config_file)
    monkeypatch.setattr("pioneers_cli.config.PIONEERS_DIR", tmp_path)

    config = PioneersConfig(backend="cloud")
    save_config(config)

    loaded = load_config()
    assert loaded.backend == "cloud"


def test_credentials_file_permissions(tmp_path, monkeypatch):
    creds_file = tmp_path / "credentials.json"
    monkeypatch.setattr("pioneers_cli.config.CREDENTIALS_FILE", creds_file)
    monkeypatch.setattr("pioneers_cli.config.PIONEERS_DIR", tmp_path)

    creds = Credentials(access_token="ghp_secret", username="user")
    save_credentials(creds)

    # Credentials file should be readable only by owner
    mode = creds_file.stat().st_mode & 0o777
    assert mode == 0o600
