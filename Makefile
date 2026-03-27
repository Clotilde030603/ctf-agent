.PHONY: challenge bootstrap-skills bootstrap-env triage session-capture session-open validate

NAME ?=
CATEGORY ?=misc
BROWSER ?=chromium
STATE ?=.auth/manual-login.playwright-state.json

challenge:
	@test -n "$(NAME)" || (printf "Usage: make challenge NAME=<challenge-name> [CATEGORY=web|pwn|rev|crypto|forensics|misc]\n" && exit 1)
	python3 scripts/new_challenge.py "$(NAME)" --category "$(CATEGORY)"

bootstrap-skills:
	bash scripts/bootstrap_lobehub_skills.sh

bootstrap-env:
	bash scripts/bootstrap_ctf_env.sh

triage:
	@test -n "$(NAME)" || (printf "Usage: make triage NAME=<challenge-name>\n" && exit 1)
	python3 scripts/triage_ctf.py "challenges/$(NAME)"

session-capture:
	@test -n "$(LOGIN_URL)" || (printf "Usage: make session-capture LOGIN_URL=<login-url> [STATE=.auth/manual-login.playwright-state.json] [BROWSER=chromium]\n" && exit 1)
	python3 scripts/capture_browser_session.py "$(LOGIN_URL)" "$(STATE)" --browser "$(BROWSER)"

session-open:
	@test -n "$(PAGE_URL)" || (printf "Usage: make session-open PAGE_URL=<page-url> [STATE=.auth/manual-login.playwright-state.json] [BROWSER=chromium]\n" && exit 1)
	python3 scripts/open_authenticated_page.py "$(PAGE_URL)" "$(STATE)" --browser "$(BROWSER)"

validate:
	python3 -m py_compile browser_session.py scripts/new_challenge.py scripts/triage_ctf.py scripts/capture_browser_session.py scripts/open_authenticated_page.py tools/exploit_template.py tools/crypto_template.py tools/solver_template.py
	python3 -m json.tool opencode.json >/dev/null
