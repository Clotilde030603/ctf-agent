.PHONY: challenge bootstrap-skills bootstrap-env triage validate

NAME ?=
CATEGORY ?=misc

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

validate:
	python3 -m py_compile scripts/new_challenge.py scripts/triage_ctf.py tools/exploit_template.py tools/crypto_template.py
	python3 -m json.tool opencode.json >/dev/null
