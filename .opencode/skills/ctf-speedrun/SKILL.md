---
name: ctf-speedrun
description: Drive a time-boxed CTF solve by prioritizing high-signal actions, cutting dead ends quickly, and switching to automation as soon as a lead appears.
license: MIT
compatibility: opencode
---

# CTF Speedrun

## What I do

- Optimize for time-to-first-breakthrough.
- Force early triage, aggressive prioritization, and fast abandonment of low-signal ideas.
- Push the workflow toward automation instead of repetitive manual poking.

## When to use me

Use this whenever the user cares more about solving within the contest clock than about perfect elegance.

## Time-boxing rules

1. Spend the first few minutes only on triage and category detection.
2. Pick the top one or two attack paths and ignore the rest initially.
3. If a path produces no new signal after a short test cycle, downgrade it immediately.
4. The moment interaction becomes repetitive, write a script.
5. If a partial primitive appears, exploit that path before exploring something prettier.

## Operating rules

- Prefer evidence-rich actions: triage, source review, strings, metadata, protocol capture, fast enumeration.
- Prefer shortest exploit path over most general exploit path.
- Do not over-document during the active solve; keep notes minimal but factual.
- If stuck, reclassify the challenge instead of blindly digging deeper.

## Escalation guide

- Web challenge stuck: shift from browser interaction to source or request replay.
- Pwn challenge stuck: shift from full exploit ambition to primitive proof and leak gathering.
- Rev challenge stuck: rewrite the smallest critical logic block into Python.
- Crypto challenge stuck: verify whether it is actually just encoding or a custom transform.
- Forensics challenge stuck: go back to containers, metadata, and extraction order.
