# CTF AI Agent for OpenCode

This repository sets up a CTF-focused OpenCode environment built around local skills and compatible with LobeHub-style skill workflows.

## What is included

- `.opencode/skills/ctf-orchestrator/`: entry skill that triages a challenge and decides which specialist skill to load.
- `.opencode/skills/ctf-web/`: workflow for web exploitation challenges.
- `.opencode/skills/ctf-pwn/`: workflow for binary exploitation challenges.
- `.opencode/skills/ctf-rev/`: workflow for reverse engineering challenges.
- `.opencode/skills/ctf-crypto/`: workflow for cryptography challenges.
- `.opencode/skills/ctf-forensics/`: workflow for forensics and artifact analysis.
- `.opencode/skills/ctf-speedrun/`: time-boxed solving mode for fast contest work.
- `.opencode/skills/ctf-writeup/`: workflow for turning notes into a clean writeup.
- `tools/`: small helper script templates.
- `scripts/bootstrap_lobehub_skills.sh`: optional LobeHub marketplace bootstrap script.
- `scripts/new_challenge.py`: creates a clean per-challenge workspace.
- `scripts/triage_ctf.py`: creates a quick triage report from challenge files.
- `scripts/bootstrap_ctf_env.sh`: creates `.venv` and installs Python CTF packages.
- `Makefile`: shortcut commands for common setup and challenge initialization.
- `challenges/`: working directory for challenge files.
- `opencode.json`: local skill permission rules for OpenCode.

## Why this structure

OpenCode skills are plain `SKILL.md` files under `.opencode/skills/<name>/SKILL.md`.
That makes local CTF specialization easy: you can keep reusable solving instructions in-repo, version them, and add challenge-specific helper scripts next to them.

LobeHub can still be used as a source of extra skills. This repo is set up so you can keep core CTF workflows locally, then install additional marketplace skills when needed.

## Quick start

1. Put challenge files under `challenges/<event-or-name>/`.
2. Optionally run `make bootstrap-env` once.
3. Start OpenCode in this repository.
4. Ask the agent to load `ctf-orchestrator` first.
5. Let it route into `ctf-web`, `ctf-pwn`, `ctf-rev`, `ctf-crypto`, or `ctf-forensics`.

Or create a fresh workspace first:

```bash
make challenge NAME=picoctf-web-001
make triage NAME=picoctf-web-001
```

Example prompts:

```text
Load the ctf-orchestrator skill and triage the files in challenges/test-web/.
```

```text
Use ctf-pwn to analyze this ELF in challenges/pwn1/ and build a pwntools exploit.
```

```text
Use ctf-crypto to inspect this ciphertext and identify likely attack paths.
```

## Recommended workflow

1. Run `make challenge NAME=<name> CATEGORY=<guess>`.
2. Drop files into `challenges/<name>/files/`.
3. Run `make triage NAME=<name>` to generate `triage.json`.
4. Run `ctf-orchestrator` and, when time matters, follow `ctf-speedrun` behavior.
5. Load the specialist skill for the category.
6. Keep notes, extracted indicators, scripts, and outputs under that challenge directory.
7. When solved, load `ctf-writeup` to turn the notes into a final writeup.

## Browser session workflow (semi-automatic authentication)

Some CTF challenges require an authenticated browser session to access post-login functionality. This framework supports a **manual-login, automated-reuse** model that keeps credentials secure while enabling browser automation.

### Why manual login?

- **Security**: Credentials are never hardcoded, logged, or transmitted to the agent
- **Control**: You perform MFA, CAPTCHA, or any custom login flow yourself
- **Safety**: Session state files are automatically excluded from git (see `.gitignore`)

### How it works

1. **Capture**: Launch a headed browser, manually log in, then save the session storage state
2. **Reuse**: Automated scripts load the saved session state and continue with authenticated requests
3. **Scope**: Session files are stored per-challenge and never committed

### Setup (one-time)

```bash
# Install project dependencies and the Playwright browser
make bootstrap-env
```

### Session capture workflow

```bash
# 1. Create a challenge workspace
make challenge NAME=htb-web-session CATEGORY=web

# 2. Launch the manual login helper (opens a headed browser)
python3 scripts/capture_browser_session.py https://challenge.htb/login \
    challenges/htb-web-session/.auth/storage.playwright-state.json

# 3. Manually log in through the browser window
# 4. Press Enter in the terminal to save the session state
# 5. The session file is now available for automation
```

### Using saved sessions in exploits

```python
# Example: Reuse session in a solve script
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(storage_state="challenges/htb-web-session/.auth/storage.playwright-state.json")
    page = context.new_page()
    
    # Already authenticated - proceed with the challenge
    page.goto("https://challenge.htb/dashboard")
    # ... exploit logic here
```

### Session management commands

```bash
# Capture a new session (manual login)
python3 scripts/capture_browser_session.py <LOGIN_URL> <STATE_PATH>

# Open an authenticated page using a previously saved state
python3 scripts/open_authenticated_page.py <PAGE_URL> <STATE_PATH>

# Makefile shortcuts
make session-capture LOGIN_URL=<LOGIN_URL> STATE=<STATE_PATH>
make session-open PAGE_URL=<PAGE_URL> STATE=<STATE_PATH>
```

### Important notes

- **Session files are sensitive**: They contain cookies, localStorage, and authentication tokens
- **Never commit sessions**: The `.gitignore` already excludes `.auth/`, `*.playwright-state.json`, and `*.auth-state.json`
- **Session expiration**: Saved sessions may expire; re-run capture if authentication fails
- **Challenge scope**: Store sessions within the challenge directory or top-level `.auth/` for organization
- **Headed vs headless**: Capture always uses headed mode; automation uses headless by default

### Integration with ctf-web skill

When working on authenticated web challenges:

1. Load `ctf-web` skill and identify the authentication requirement
2. Use `capture_browser_session.py` to perform manual login and save state
3. Reference the session path in your exploit scripts
4. The agent can automate post-login exploration and exploitation
5. Document the session workflow in `notes.md` for reproducibility

## Adding LobeHub skills

Search for additional CTF skills:

```bash
npx -y @lobehub/market-cli skills search --q "ctf"
```

You can then install useful marketplace skills globally and keep these local skills as your base workflow.

To bootstrap a practical default set, run:

```bash
bash scripts/bootstrap_lobehub_skills.sh
```

The script is conservative: it checks for `npx`, shows what it is about to install, and keeps local repo skills as the primary workflow.

## Practical commands

```bash
make challenge NAME=htb-rev-100
make challenge NAME=pico-web-02 CATEGORY=web
make triage NAME=htb-rev-100
make bootstrap-env
python3 scripts/new_challenge.py crewctf-pwn-01 --category pwn
```

Once files are in place, ask OpenCode something like:

```text
Load ctf-orchestrator, inspect challenges/htb-rev-100/, read triage.json if present, classify the challenge, and continue with the best matching specialist skill in speedrun mode.
```

## Suggested challenge layout

```text
challenges/
  picoctf-web-001/
    README.md
    notes.md
    plan.md
    files/
    solve.py
    triage.json
    artifacts/
```

## Tooling assumptions

This repo assumes the agent can use shell and read/write tools responsibly. For practical CTF work, common local tools help a lot:

- Python 3
- `venv`
- `requests`
- `pwntools`
- `pycryptodome`
- `playwright` (for browser automation - see Browser session workflow)
- `binwalk`
- `strings`, `file`, `xxd`
- `gdb` or `lldb`
- `checksec`
- `radare2` or Ghidra

These are not auto-installed here because environments differ, but the skill files are written to take advantage of them when available.

## Files to customize

- `opencode.json`: adjust what skills are auto-allowed.
- `.opencode/skills/*/SKILL.md`: tune challenge methodology to your preference.
- `scripts/bootstrap_lobehub_skills.sh`: change the marketplace skills you want preinstalled.
- `scripts/new_challenge.py`: change the folder template for your workflow.
- `browser_session.py`: customize shared browser launch, state validation, and session capture behavior.
- `scripts/capture_browser_session.py`: adjust the manual login capture CLI.
- `scripts/open_authenticated_page.py`: adjust the authenticated browser-open CLI.
- `tools/`: add helper scripts you use repeatedly.
- `.gitignore`: ensure session state directories are excluded if you modify storage paths.

## Goal

The goal is not just to add prompts. It is to give OpenCode a repeatable CTF operating environment: triage, specialized workflows, challenge workspace discipline, and reusable solve templates.
