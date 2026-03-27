#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from browser_session import DEFAULT_BROWSER, SUPPORTED_BROWSERS, open_authenticated_page


def positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return parsed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Open a visible browser page with an existing Playwright storage state.",
    )
    parser.add_argument("target_url", help="absolute page URL to open with the saved auth state")
    parser.add_argument(
        "state_path",
        help="path to an existing storage state JSON file captured earlier",
    )
    parser.add_argument(
        "--browser",
        choices=SUPPORTED_BROWSERS,
        default=DEFAULT_BROWSER,
        help="Playwright browser to launch (default: %(default)s)",
    )
    parser.add_argument(
        "--ready-url",
        help="optional Playwright wait_for_url pattern checked after the page opens",
    )
    parser.add_argument(
        "--ready-selector",
        help="optional selector that must appear before the script hands control to you",
    )
    parser.add_argument(
        "--timeout",
        type=positive_float,
        default=30.0,
        help="seconds to wait for optional ready checks (default: %(default)s)",
    )
    args = parser.parse_args()

    open_authenticated_page(
        args.target_url,
        args.state_path,
        browser_name=args.browser,
        ready_url=args.ready_url,
        ready_selector=args.ready_selector,
        timeout_seconds=args.timeout,
    )


if __name__ == "__main__":
    main()
