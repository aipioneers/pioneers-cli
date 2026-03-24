"""Tests for CLI commands."""

from typer.testing import CliRunner

from pioneers_cli.cli import app

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "pioneers-cli" in result.output


def test_status_not_logged_in(tmp_path, monkeypatch):
    monkeypatch.setattr("pioneers_cli.config.CREDENTIALS_FILE", tmp_path / "creds.json")
    monkeypatch.setattr("pioneers_cli.config.CONFIG_FILE", tmp_path / "config.json")
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "not logged in" in result.output


def test_logout_not_logged_in(tmp_path, monkeypatch):
    monkeypatch.setattr("pioneers_cli.config.CREDENTIALS_FILE", tmp_path / "creds.json")
    result = runner.invoke(app, ["logout"])
    assert result.exit_code == 0
    assert "Not logged in" in result.output


def test_config_get_backend(tmp_path, monkeypatch):
    monkeypatch.setattr("pioneers_cli.config.CONFIG_FILE", tmp_path / "config.json")
    monkeypatch.setattr("pioneers_cli.config.PIONEERS_DIR", tmp_path)
    result = runner.invoke(app, ["config", "backend"])
    assert result.exit_code == 0
    assert "local" in result.output


def test_config_set_backend(tmp_path, monkeypatch):
    monkeypatch.setattr("pioneers_cli.config.CONFIG_FILE", tmp_path / "config.json")
    monkeypatch.setattr("pioneers_cli.config.PIONEERS_DIR", tmp_path)
    result = runner.invoke(app, ["config", "backend", "cloud"])
    assert result.exit_code == 0
    assert "cloud" in result.output


def test_config_set_invalid_backend(tmp_path, monkeypatch):
    monkeypatch.setattr("pioneers_cli.config.CONFIG_FILE", tmp_path / "config.json")
    monkeypatch.setattr("pioneers_cli.config.PIONEERS_DIR", tmp_path)
    result = runner.invoke(app, ["config", "backend", "invalid"])
    assert result.exit_code == 1


def test_config_unknown_key(tmp_path, monkeypatch):
    monkeypatch.setattr("pioneers_cli.config.CONFIG_FILE", tmp_path / "config.json")
    result = runner.invoke(app, ["config", "nonexistent"])
    assert result.exit_code == 1
