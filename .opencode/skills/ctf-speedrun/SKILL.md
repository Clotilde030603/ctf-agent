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

1. Spend the first 2-3 minutes only on parallel triage and category detection.
2. Pick the top 2-3 attack paths and run them as parallel lanes; ignore the rest initially.
3. If a lane produces no new signal after 2-3 minutes, kill it immediately (no exceptions).
4. The moment interaction becomes repetitive (2+ identical steps), write a script immediately.
5. If a partial primitive appears, exploit that path before exploring something prettier.
6. Total challenge budget: 15-20 minutes for easy/medium, 30-40 for hard; enforce strictly.

## Parallel lanes

Speedrun mode aggressively parallelizes discovery to minimize time-to-flag:

### Lane limits
- Maximum 4 lanes total (including triage tools).
- Typical split: 2-3 hypothesis lanes + 1 tool lane.
- Never run more than 3 hypothesis lanes simultaneously.

### Spawn rules
- Spawn lanes when attack surface is genuinely unclear (category ambiguous, multiple entry points).
- Spawn lanes when different bug classes have similar likelihood (e.g., SQLi vs path traversal vs IDOR).
- Spawn tool lanes immediately: `file`, `strings`, `binwalk`, `exiftool`, `checksec` in parallel.

### Time budgets (strict)
- Triage tool lane: 30-60 seconds total.
- Individual hypothesis lane: 2-3 minutes max.
- No extensions; kill at budget expiration regardless of "almost there" status.

### Merge triggers (merge immediately when any occur)
- Flag fragment or candidate recovered.
- Vulnerability confirmed with reproducible PoC.
- Exploit primitive identified (leak, write, read, control flow).
- Category definitively identified with evidence.

### Kill triggers (abandon lane immediately)
- Time budget expires with no actionable signal.
- 3+ consecutive probes return identical negative results.
- Lane requires preconditions proven impossible by another lane.
- Another lane has merged and is progressing toward flag.

### Automation triggers (switch to script immediately)
- Same request/operation repeated 2+ times.
- Brute force or enumeration space identified.
- Encoding/decoding pattern confirmed.
- Network interaction becomes non-trivial (3+ steps).

## Operating rules

- Prefer evidence-rich actions: triage, source review, strings, metadata, protocol capture, fast enumeration.
- Prefer shortest exploit path over most general exploit path.
- Do not over-document during the active solve; keep notes minimal but factual.
- If stuck, reclassify the challenge instead of blindly digging deeper.
- **Serial work is forbidden**: If two investigations are independent, they must run in parallel.
- **Evidence threshold**: A lane lives or dies based on signal, not potential; no "just one more try".
- **Script everything**: Manual repetition is a speedrun failure; automate at first repetition.
- **Merge ruthlessly**: When one lane succeeds, kill others immediately and focus all resources on the winning path.

## Escalation guide

- Web challenge stuck: shift from browser interaction to source or request replay.
- Pwn challenge stuck: shift from full exploit ambition to primitive proof and leak gathering.
- Rev challenge stuck: rewrite the smallest critical logic block into Python.
- Crypto challenge stuck: verify whether it is actually just encoding or a custom transform.
- Forensics challenge stuck: go back to containers, metadata, and extraction order.
