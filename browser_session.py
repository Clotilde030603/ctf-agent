#!/usr/bin/env python3

from __future__ import annotations

import importlib
from pathlib import Path
import sys
from typing import Any
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_BROWSER = "chromium"
SUPPORTED_BROWSERS = ("chromium", "firefox", "webkit")
IGNORED_SESSION_DIRECTORY = ".auth"
IGNORED_SESSION_SUFFIXES = (".playwright-state.json", ".auth-state.json")


def validate_web_url(url: str, *, label: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"{label} must be an absolute http(s) URL: {url}")
    return url


def require_interactive_terminal() -> None:
    if not sys.stdin.isatty():
        raise SystemExit("manual browser session commands require an interactive terminal")


def ensure_repo_session_path_is_ignored(state_path: Path) -> None:
    try:
        relative_path = state_path.relative_to(REPO_ROOT)
    except ValueError:
        return

    if relative_path.parts and relative_path.parts[0] == IGNORED_SESSION_DIRECTORY:
        return
    if any(relative_path.name.endswith(suffix) for suffix in IGNORED_SESSION_SUFFIXES):
        return

    raise ValueError(
        "session state files inside this repo must live under .auth/ or end with "
        ".playwright-state.json / .auth-state.json so git ignores them"
    )


def resolve_state_path(raw_path: str, *, must_exist: bool) -> Path:
    state_path = Path(raw_path).expanduser()
    if not state_path.is_absolute():
        state_path = Path.cwd() / state_path
    state_path = state_path.resolve(strict=False)

    if state_path.exists() and state_path.is_dir():
        raise ValueError(f"state path must be a file, not a directory: {state_path}")

    ensure_repo_session_path_is_ignored(state_path)

    if must_exist and not state_path.exists():
        raise FileNotFoundError(f"state file does not exist: {state_path}")
    if not must_exist:
        state_path.parent.mkdir(parents=True, exist_ok=True)

    return state_path


def load_playwright() -> tuple[Any, type[Exception], type[Exception]]:
    try:
        sync_api = importlib.import_module("playwright.sync_api")
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Playwright is not installed. Run `pip install -r requirements.txt` first."
        ) from exc
    return sync_api.sync_playwright, sync_api.Error, sync_api.TimeoutError


def resolve_browser_type(playwright: Any, browser_name: str) -> Any:
    if browser_name not in SUPPORTED_BROWSERS:
        raise ValueError(
            f"unsupported browser '{browser_name}'. Choose from: {', '.join(SUPPORTED_BROWSERS)}"
        )
    return getattr(playwright, browser_name)


def wait_for_optional_ready_state(
    page: Any,
    *,
    ready_url: str | None,
    ready_selector: str | None,
    timeout_seconds: float,
) -> None:
    timeout_ms = max(1, int(timeout_seconds * 1000))
    if ready_url:
        page.wait_for_url(ready_url, timeout=timeout_ms)
    if ready_selector:
        page.locator(ready_selector).first.wait_for(timeout=timeout_ms)


def prompt_for_manual_login() -> None:
    print("Manual login only: enter credentials in the visible browser window, not in this script.")
    try:
        input("Press Enter here after the authenticated browser session is ready to save... ")
    except EOFError as exc:
        raise SystemExit("interactive confirmation failed because stdin is closed") from exc


def hold_authenticated_browser_open() -> None:
    try:
        input("Authenticated browser is open. Press Enter here to close it... ")
    except EOFError as exc:
        raise SystemExit("interactive confirmation failed because stdin is closed") from exc


def format_playwright_error(exc: Exception, *, browser_name: str) -> str:
    message = str(exc)
    if "Executable doesn't exist" in message:
        return (
            f"{message}\nInstall the browser with `python -m playwright install {browser_name}`."
        )
    return message


def capture_manual_login_session(
    login_url: str,
    state_path: str,
    *,
    browser_name: str = DEFAULT_BROWSER,
    ready_url: str | None = None,
    ready_selector: str | None = None,
    timeout_seconds: float = 30.0,
) -> Path:
    require_interactive_terminal()
    validate_web_url(login_url, label="login URL")
    resolved_state_path = resolve_state_path(state_path, must_exist=False)

    sync_playwright, playwright_error, playwright_timeout = load_playwright()
    try:
        with sync_playwright() as playwright:
            browser = resolve_browser_type(playwright, browser_name).launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto(login_url, wait_until="domcontentloaded")
            print(f"Opened login page: {login_url}")
            prompt_for_manual_login()
            wait_for_optional_ready_state(
                page,
                ready_url=ready_url,
                ready_selector=ready_selector,
                timeout_seconds=timeout_seconds,
            )
            context.storage_state(path=str(resolved_state_path))
            browser.close()
    except playwright_timeout as exc:
        raise SystemExit(f"login ready-state check timed out: {exc}") from exc
    except playwright_error as exc:
        raise SystemExit(format_playwright_error(exc, browser_name=browser_name)) from exc
    except KeyboardInterrupt as exc:
        raise SystemExit("cancelled by user") from exc

    print(f"Saved authenticated storage state to {resolved_state_path}")
    return resolved_state_path


def open_authenticated_page(
    target_url: str,
    state_path: str,
    *,
    browser_name: str = DEFAULT_BROWSER,
    ready_url: str | None = None,
    ready_selector: str | None = None,
    timeout_seconds: float = 30.0,
) -> Path:
    require_interactive_terminal()
    validate_web_url(target_url, label="target URL")
    resolved_state_path = resolve_state_path(state_path, must_exist=True)

    sync_playwright, playwright_error, playwright_timeout = load_playwright()
    try:
        with sync_playwright() as playwright:
            browser = resolve_browser_type(playwright, browser_name).launch(headless=False)
            context = browser.new_context(storage_state=str(resolved_state_path))
            page = context.new_page()
            page.goto(target_url, wait_until="domcontentloaded")
            wait_for_optional_ready_state(
                page,
                ready_url=ready_url,
                ready_selector=ready_selector,
                timeout_seconds=timeout_seconds,
            )
            print(f"Opened authenticated page: {target_url}")
            hold_authenticated_browser_open()
            browser.close()
    except playwright_timeout as exc:
        raise SystemExit(f"authenticated page ready-state check timed out: {exc}") from exc
    except playwright_error as exc:
        raise SystemExit(format_playwright_error(exc, browser_name=browser_name)) from exc
    except KeyboardInterrupt as exc:
        raise SystemExit("cancelled by user") from exc

    return resolved_state_path


__all__ = [
    "DEFAULT_BROWSER",
    "SUPPORTED_BROWSERS",
    "capture_manual_login_session",
    "open_authenticated_page",
    "resolve_state_path",
    "validate_web_url",
]
