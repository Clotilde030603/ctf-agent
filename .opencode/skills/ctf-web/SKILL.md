---
name: ctf-web
description: Solve CTF web challenges by mapping the app, identifying attack surface, testing hypotheses, and turning wins into reproducible exploits.
license: MIT
compatibility: opencode
---

# CTF Web

## What I do

- Map routes, parameters, cookies, headers, and authentication flow.
- Inspect frontend and backend code if source is provided.
- Test common CTF bug classes: injection, auth bypass, SSTI, deserialization, path traversal, SSRF, XSS, CSRF, IDOR, and unsafe file handling.
- Write short exploit scripts when manual repetition becomes slow.

## When to use me

Use this for websites, APIs, source bundles, containers exposing HTTP services, or browser-based challenges.

## Workflow

1. Identify the app stack and entrypoints.
2. Enumerate user-controlled input.
3. Look for trust boundaries and places where user input reaches sensitive operations.
4. Test the smallest high-signal hypotheses first.
5. Save working requests and proof-of-concept scripts under the challenge directory.

## Parallel lanes

Web apps expose multiple attack surfaces simultaneously. Run parallel discovery lanes where they do not interfere:
- Lane A: Source and configuration review (routes, filters, secrets in code).
- Lane B: Endpoint enumeration and parameter fuzzing (hidden routes, debug endpoints).
- Lane C: Injection testing on the highest-surface inputs (SQL, SSTI, command) with small probes.
- Lane D: Authentication/session analysis (JWT, cookies, headers) for bypass opportunities.
Merge when a lane confirms a vulnerability class; abandon lanes that return consistent negatives after quick tests.

## High-value checks

- Template injection indicators such as reflected evaluation syntax.
- File path joins and download endpoints.
- JWT, session, and cookie validation mistakes.
- Hidden routes, admin-only behavior, and object identifiers.
- Debug endpoints, source maps, backups, and `.git` exposure.
- Filter bypasses via encoding, content type changes, and parser differentials.

## Rules

- Prefer evidence from responses over assumptions.
- Keep a reproducible request trail.
- When fuzzing, control the rate and document what changed.
- If you get code execution or file read, pivot carefully toward flag locations and secrets.
