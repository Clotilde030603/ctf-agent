#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from browser_session import DEFAULT_BROWSER, SUPPORTED_BROWSERS, capture_manual_login_session


def positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return parsed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Open a visible browser for manual login and save Playwright storage state.",
    )
    parser.add_argument("login_url", help="absolute login URL to open in the browser")
    parser.add_argument(
        "state_path",
        help="path for the saved storage state JSON (inside the repo use .auth/ or a *.playwright-state.json name)",
    )
    parser.add_argument(
        "--browser",
        choices=SUPPORTED_BROWSERS,
        default=DEFAULT_BROWSER,
        help="Playwright browser to launch (default: %(default)s)",
    )
    parser.add_argument(
        "--ready-url",
        help="optional Playwright wait_for_url pattern checked after you confirm login",
    )
    parser.add_argument(
        "--ready-selector",
        help="optional selector that must appear before the session state is saved",
    )
    parser.add_argument(
        "--timeout",
        type=positive_float,
        default=30.0,
        help="seconds to wait for optional ready checks (default: %(default)s)",
    )
    args = parser.parse_args()

    capture_manual_login_session(
        args.login_url,
        args.state_path,
        browser_name=args.browser,
        ready_url=args.ready_url,
        ready_selector=args.ready_selector,
        timeout_seconds=args.timeout,
    )


if __name__ == "__main__":
    main()
