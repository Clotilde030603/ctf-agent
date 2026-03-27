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

## Parallel lanes

Reverse engineering benefits from multiple simultaneous analysis angles:

### Lane definitions
- Lane A: Decompiler-assisted high-level logic recovery (validation, encoding chains).
- Lane B: Disassembly-focused instruction tracing for anti-debug, packers, or VM handlers.
- Lane C: Dynamic analysis for input/output behavior and state changes.
- Lane D: String and data table extraction for hardcoded constants, keys, or flag fragments.

### Lane budgets
- Maximum 3 lanes concurrently.
- Lane A: 5 minutes; if decompilation fails or produces garbage, pivot to Lane B.
- Lane B: 10 minutes for targeted function analysis.
- Lane C: 5 minutes or until 10+ test inputs executed.
- Lane D: 2 minutes (fast string/table extraction).

### Decompiler vs dynamic thresholds
- Use decompiler first for <500KB binaries without packing.
- Switch to dynamic (Lane C) if: anti-debug detected, heavy obfuscation, or decompiler output is incomprehensible after 5 minutes.
- Use disassembly (Lane B) for packers, VMs, or when specific instructions matter.

### Merge criteria
- Complete transformation algorithm recovered.
- Flag fragment found in strings/data tables.
- Input/output behavior mapped to validation logic.
- VM instruction handler or packer stub identified.

### Kill criteria
- Decompiler produces no useful output after 5 minutes (switch to dynamic).
- Anti-debug prevents dynamic analysis and no bypass found after 10 minutes.
- String extraction returns no flag-like patterns and no cryptographic material.
- Another lane has fully recovered the transformation logic.

### Automation triggers
- Input brute force against validation function.
- Automated deobfuscation of simple transforms.
- Batch testing of decoded strings against flag format.
- Symbolic execution for path exploration.

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
