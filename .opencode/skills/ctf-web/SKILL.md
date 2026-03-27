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

### Lane definitions
- Lane A: Source and configuration review (routes, filters, secrets in code).
- Lane B: Endpoint enumeration and parameter fuzzing (hidden routes, debug endpoints).
- Lane C: Injection testing on the highest-surface inputs (SQL, SSTI, command) with small probes.
- Lane D: Authentication/session analysis (JWT, cookies, headers) for bypass opportunities.

### Lane budgets
- Maximum 3 lanes running concurrently.
- 5 minutes per lane before requiring evidence.
- If source is provided, prioritize Lane A first but run Lane B in parallel.

### Merge criteria
- Vulnerability confirmed with reproducible PoC.
- Authentication bypass or privilege escalation identified.
- Source code reveals clear exploit path.
- Flag or sensitive data accessed.

### Kill criteria
- 10+ consecutive endpoints return 404/403 with no anomalies.
- 5+ injection probes return identical safe responses.
- JWT/session analysis confirms proper validation with no bypass.
- Another lane has merged with a working exploit path.

### Automation triggers
- More than 3 similar requests (fuzzing, parameter testing).
- Enumeration of routes, IDs, or files.
- Session/token manipulation testing.
- Any repetitive HTTP interaction.

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
