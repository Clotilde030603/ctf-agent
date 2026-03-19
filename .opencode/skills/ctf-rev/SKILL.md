---
name: ctf-rev
description: Solve reverse engineering challenges by reconstructing program logic, recovering transformations, and building scripts to automate the solution.
license: MIT
compatibility: opencode
---

# CTF Reverse Engineering

## What I do

- Inspect binaries, scripts, bytecode, and packed artifacts.
- Recover validation logic and hidden transformations.
- Rename concepts clearly and turn manual reversing into scripts.
- Extract candidate flags or input constraints.

## When to use me

Use this for crackmes, key checks, obfuscated scripts, custom virtual machines, or challenge binaries where logic matters more than memory corruption.

## Workflow

1. Identify the executable format and runtime.
2. Find the real entry logic and ignore boilerplate.
3. Locate comparisons, decoding pipelines, and data tables.
4. Rewrite the important logic into a small script.
5. Validate the reconstructed logic against the binary or samples.

## High-value patterns

- XOR/add/sub rotation pipelines.
- Lookup tables and substitution boxes.
- Length checks and segmented validators.
- State machines and custom bytecode interpreters.
- Packers, anti-debug checks, and dead-code noise.

## Rules

- Prefer naming by behavior, not by guessed intent.
- Recreate transforms exactly before simplifying them.
- Keep a map from addresses or functions to roles.
- If a decompiler view is confusing, drop to disassembly for the critical block.
