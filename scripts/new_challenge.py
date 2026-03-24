#!/usr/bin/env python3

import argparse
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"

CATEGORY_PROMPTS = {
    "web": "Start with ctf-orchestrator, then likely route into ctf-web.",
    "pwn": "Start with ctf-orchestrator, then likely route into ctf-pwn.",
    "rev": "Start with ctf-orchestrator, then likely route into ctf-rev.",
    "crypto": "Start with ctf-orchestrator, then likely route into ctf-crypto.",
    "forensics": "Start with ctf-orchestrator, then likely route into ctf-forensics.",
    "misc": "Start with ctf-orchestrator and let it classify the challenge.",
}

SOLVE_TEMPLATES = {
    "crypto": "crypto_template.py",
    "pwn": "exploit_template.py",
}

DEFAULT_SOLVE_TEMPLATE = "solver_template.py"


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def load_solve_template(category: str) -> str:
    template_name = SOLVE_TEMPLATES.get(category, DEFAULT_SOLVE_TEMPLATE)
    return (TOOLS_DIR / template_name).read_text(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a CTF challenge workspace")
    parser.add_argument("name", help="challenge directory name under challenges/")
    parser.add_argument(
        "--category",
        default="misc",
        choices=sorted(CATEGORY_PROMPTS),
        help="likely challenge category",
    )
    args = parser.parse_args()

    base = Path("challenges") / args.name
    files_dir = base / "files"
    artifacts_dir = base / "artifacts"

    files_dir.mkdir(parents=True, exist_ok=True)
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    write_if_missing(
        base / "README.md",
        f"# {args.name}\n\n"
        f"- Category guess: `{args.category}`\n"
        f"- Workflow hint: {CATEGORY_PROMPTS[args.category]}\n\n"
        "## Prompt\n\n"
        "Paste the original challenge statement here.\n",
    )
    write_if_missing(
        base / "notes.md",
        "# Notes\n\n"
        "## Timer\n\n"
        "- Start time:\n"
        "- Deadline:\n"
        "- Current best lead:\n\n"
        "## Facts\n\n"
        "## Hypotheses\n\n"
        "## Disproved ideas\n\n"
        "## Useful commands\n\n"
        "## Flag candidates\n",
    )
    write_if_missing(
        base / "plan.md",
        "# Rapid Plan\n\n"
        "1. Run triage and classify the challenge.\n"
        "2. Pursue the highest-signal attack path first.\n"
        "3. Automate repeated interaction quickly.\n"
        "4. Validate flag format before declaring success.\n",
    )
    write_if_missing(
        base / "solve.py",
        load_solve_template(args.category),
    )

    print(f"created workspace: {base}")


if __name__ == "__main__":
    main()
