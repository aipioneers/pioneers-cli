"""CLI entry point for the pioneers command."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from pioneers_cli import __version__
from pioneers_cli.auth import device_flow_login, get_current_user
from pioneers_cli.config import (
    delete_credentials,
    load_config,
    save_config,
    PioneersConfig,
)

app = typer.Typer(
    name="pioneers",
    help="AI Pioneers CLI — authenticate and configure cloud features.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def login() -> None:
    """Authenticate with your AI Pioneers account via GitHub."""
    existing = get_current_user()
    if existing:
        console.print(f"Already logged in as [bold]@{existing.username}[/bold].")
        if not typer.confirm("Log in again?"):
            raise typer.Exit()

    creds = device_flow_login()
    if creds:
        console.print(f"\n[green]Logged in as [bold]@{creds.username}[/bold].[/green]")
        console.print("[dim]Tip: Run `cex config set backend cloud` to use cloud search.[/dim]")
    else:
        console.print("[red]Login failed.[/red]")
        raise typer.Exit(code=1)


@app.command()
def logout() -> None:
    """Remove stored credentials."""
    if delete_credentials():
        console.print("[green]Logged out.[/green]")
    else:
        console.print("[dim]Not logged in.[/dim]")


@app.command()
def status() -> None:
    """Show current authentication and configuration status."""
    creds = get_current_user()
    config = load_config()

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold")
    table.add_column()

    if creds:
        table.add_row("User", f"@{creds.username}")
        table.add_row("Email", creds.email or "—")
        table.add_row("Plan", creds.plan)
    else:
        table.add_row("User", "[dim]not logged in[/dim]")

    table.add_row("Backend", config.backend)
    table.add_row("API", config.api_url)

    console.print(table)


@app.command()
def config(
    key: str = typer.Argument(help="Config key: backend, api_url"),
    value: str = typer.Argument(default=None, help="Value to set. Omit to show current value."),
) -> None:
    """Get or set a configuration value."""
    cfg = load_config()

    if value is None:
        # Get
        val = getattr(cfg, key, None)
        if val is None:
            console.print(f"[red]Unknown key: {key}[/red]")
            raise typer.Exit(code=1)
        console.print(val)
    else:
        # Set
        if key == "backend":
            if value not in ("local", "cloud"):
                console.print("[red]Backend must be 'local' or 'cloud'.[/red]")
                raise typer.Exit(code=1)
            cfg.backend = value
        elif key == "api_url":
            cfg.api_url = value
        else:
            console.print(f"[red]Unknown key: {key}[/red]")
            raise typer.Exit(code=1)

        save_config(cfg)
        console.print(f"[green]{key} = {value}[/green]")


@app.command()
def version() -> None:
    """Show version."""
    console.print(f"pioneers-cli {__version__}")


if __name__ == "__main__":
    app()
