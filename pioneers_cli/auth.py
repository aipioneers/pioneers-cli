"""GitHub OAuth device flow authentication."""

from __future__ import annotations

import time
import webbrowser

import httpx
from rich.console import Console
from rich.panel import Panel

from pioneers_cli.config import (
    AUTH_URL,
    API_BASE_URL,
    Credentials,
    save_credentials,
    load_credentials,
)

console = Console()

# GitHub OAuth App (public client ID — safe to embed)
GITHUB_CLIENT_ID = "Ov23liIuROAFVHawEcCE"
GITHUB_DEVICE_URL = "https://github.com/login/device/code"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"


def device_flow_login() -> Credentials | None:
    """Authenticate via GitHub device flow.

    Opens a browser for the user to authorize, then polls for the token.
    Returns credentials on success, None on failure/cancellation.
    """
    try:
        # Step 1: Request device code
        resp = httpx.post(
            GITHUB_DEVICE_URL,
            data={"client_id": GITHUB_CLIENT_ID, "scope": "read:user user:email"},
            headers={"Accept": "application/json"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        device_code = data["device_code"]
        user_code = data["user_code"]
        verification_uri = data["verification_uri"]
        interval = data.get("interval", 5)
        expires_in = data.get("expires_in", 900)

        # Step 2: Show code and open browser
        console.print()
        console.print(Panel(
            f"[bold]{user_code}[/bold]\n\n"
            f"Open [link={verification_uri}]{verification_uri}[/link] and enter the code above.",
            title="GitHub Authorization",
            border_style="blue",
        ))
        console.print()

        try:
            webbrowser.open(verification_uri)
            console.print("[dim]Browser opened. Waiting for authorization...[/dim]")
        except Exception:
            console.print(f"[dim]Open {verification_uri} in your browser.[/dim]")

        # Step 3: Poll for token
        deadline = time.time() + expires_in
        while time.time() < deadline:
            time.sleep(interval)

            token_resp = httpx.post(
                GITHUB_TOKEN_URL,
                data={
                    "client_id": GITHUB_CLIENT_ID,
                    "device_code": device_code,
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                },
                headers={"Accept": "application/json"},
                timeout=10,
            )
            token_data = token_resp.json()

            error = token_data.get("error")
            if error == "authorization_pending":
                continue
            elif error == "slow_down":
                interval += 5
                continue
            elif error:
                console.print(f"[red]Authorization failed: {error}[/red]")
                return None

            # Success — got the token
            access_token = token_data["access_token"]

            # Fetch user info
            user_resp = httpx.get(
                GITHUB_USER_URL,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/vnd.github+json",
                },
                timeout=10,
            )
            user_resp.raise_for_status()
            user_data = user_resp.json()

            creds = Credentials(
                access_token=access_token,
                username=user_data.get("login", "unknown"),
                email=user_data.get("email"),
            )

            # Register with Pioneers API (best-effort)
            _register_with_api(creds)

            save_credentials(creds)
            return creds

        console.print("[red]Authorization timed out.[/red]")
        return None

    except httpx.HTTPError as e:
        console.print(f"[red]Network error: {e}[/red]")
        return None


def _register_with_api(creds: Credentials) -> None:
    """Register the user with the Pioneers API (best-effort, non-blocking)."""
    try:
        httpx.post(
            f"{API_BASE_URL}/auth/register",
            json={"username": creds.username, "email": creds.email},
            headers={"Authorization": f"Bearer {creds.access_token}"},
            timeout=5,
        )
    except httpx.HTTPError:
        pass  # API might not be live yet — that's fine


def get_current_user() -> Credentials | None:
    """Return current logged-in user, or None."""
    return load_credentials()
