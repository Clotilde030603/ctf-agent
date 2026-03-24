---
name: ctf-misc
description: Solve mixed or miscellaneous CTF challenges by quickly identifying the real underlying technique and reducing it to a reproducible workflow.
license: MIT
compatibility: opencode
---

# CTF Misc

## What I do

- Handle miscellaneous challenges that mix encoding, scripting, protocols, automation, or puzzle logic.
- Reduce vague challenge descriptions into concrete testable components.
- Re-route to a specialist workflow if the challenge is only pretending to be misc.

## When to use me

Use this when the challenge category is unclear, mixed, or intentionally misleading.

## Workflow

1. List all observable artifacts and interfaces.
2. Identify whether the core task is really web, rev, crypto, forensics, or scripting.
3. If it is truly mixed, break the challenge into small subproblems.
4. Automate the repetitive part as soon as the core transformation is visible.
5. Keep a clean note trail so the challenge can be handed off or written up later.

## Parallel lanes

Misc challenges often hide their true category. Run multiple independent discovery lanes concurrently:
- Lane A: Quick encoding/crypto checks (entropy, base64, XOR, small-key brute).
- Lane B: File structure and container extraction (binwalk, foremost, zsteg).
- Lane C: Network/protocol artifacts if any pcap or traffic-like data exists.
- Lane D: Scripting/automation surface if the challenge presents an interactive service.
Merge when one lane produces a concrete transformation or flag fragment; abandon lanes that return only noise after initial probes.

## Rules

- Treat misc as a temporary label, not a final diagnosis.
- Prefer simple scripts over manual repetition.
- When the puzzle depends on text parsing or protocol shaping, create a minimal reproducer first.
