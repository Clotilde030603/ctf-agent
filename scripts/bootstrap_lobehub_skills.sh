#!/usr/bin/env bash
set -euo pipefail

if ! command -v npx >/dev/null 2>&1; then
  printf 'npx is required to install LobeHub marketplace skills.\n' >&2
  exit 1
fi

skills=(
  "cyberkaida-reverse-engineering-assistant-ctf-rev"
  "cyberkaida-reverse-engineering-assistant-ctf-pwn"
  "cyberkaida-reverse-engineering-assistant-ctf-crypto"
)

printf 'Bootstrapping LobeHub CTF skills...\n'
printf 'This keeps local .opencode skills as the primary workflow.\n'

for skill in "${skills[@]}"; do
  printf 'Installing %s\n' "$skill"
  npx -y @lobehub/market-cli skills install "$skill"
done

printf 'Done. You can search for more with:\n'
printf '  npx -y @lobehub/market-cli skills search --q "ctf"\n'
