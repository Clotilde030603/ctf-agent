#!/usr/bin/env bash
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  printf 'python3 is required.\n' >&2
  exit 1
fi

printf 'Creating Python virtual environment in .venv\n'
python3 -m venv .venv

printf 'Upgrading pip\n'
./.venv/bin/python -m pip install --upgrade pip setuptools wheel

printf 'Installing Python packages from requirements.txt\n'
./.venv/bin/pip install -r requirements.txt

printf 'Installing Playwright Chromium browser\n'
./.venv/bin/python -m playwright install chromium

printf 'Done. Activate with:\n'
printf '  source .venv/bin/activate\n'
