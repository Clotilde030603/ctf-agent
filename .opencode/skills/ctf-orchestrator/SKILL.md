---
name: ctf-orchestrator
description: Triage a CTF challenge, identify the likely category, choose the next specialist skill, and enforce a disciplined solving workflow.
license: MIT
compatibility: opencode
---

# CTF Orchestrator

## What I do

- Classify a challenge into web, pwn, reverse engineering, crypto, forensics, misc, or mixed.
- Inspect the available files before making claims.
- Create a short solve plan with concrete next actions.
- Decide which specialist skill should be loaded next.
- Keep notes focused on extracting evidence, not guessing.
- Use `ctf-speedrun` behavior when the priority is fast solves under time pressure.

## When to use me

Use this first when a new challenge arrives and you do not yet know the category or the right solving path.

## Workflow

1. Read the challenge prompt and list all provided files.
2. Run lightweight triage:
   - `file`, `strings`, `checksec`, `exiftool`, `binwalk`, `xxd`, or directory inspection as appropriate.
   - if available, run `python3 scripts/triage_ctf.py <challenge-dir>` and review the generated `triage.json`.
   - note filenames, formats, protections, endpoints, encodings, and any obvious indicators.
3. Decide the likely category and explain the evidence.
4. Load exactly one main specialist skill unless the challenge is clearly mixed.
5. Create a short plan with fast validation steps.
6. If a challenge directory does not exist yet, suggest using `make challenge NAME=<name> CATEGORY=<category>`.
7. If the user wants speed, apply `ctf-speedrun` rules immediately.

## Decision guide

- If there is a web app, request/response flow, source bundle, endpoint, template, or browser interaction: use `ctf-web`.
- If there is an ELF, PE, libc, network service, shellcode, crash, or memory corruption angle: use `ctf-pwn`.
- If there is an executable but the task is understanding logic rather than exploitation: use `ctf-rev`.
- If there are ciphertexts, hashes, weird encodings, modular arithmetic, or custom ciphers: use `ctf-crypto`.
- If there are disk images, pcaps, logs, Office docs, images, memory dumps, or metadata trails: use `ctf-forensics`.
- If it is unclear, puzzle-like, automation-heavy, or crosses categories: use `ctf-misc` first.
- If the main concern is contest time and rapid iteration: also load `ctf-speedrun` behavior.

## Rules

- Do not invent challenge details before reading files.
- Prefer fast triage before deep analysis.
- Keep a running list of facts, hypotheses, and disproven ideas separately.
- If the category is mixed, choose the dominant one first and say what secondary angle might matter.
- If you recover a flag candidate, validate the format instead of assuming it is final.
- If no workspace exists, tell the user exactly which `make challenge` command to run or create the structure before deeper analysis.
- Bias toward the fastest credible solve path, not the most comprehensive analysis.
