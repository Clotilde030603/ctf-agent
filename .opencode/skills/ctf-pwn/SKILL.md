---
name: ctf-pwn
description: Solve binary exploitation challenges through binary triage, mitigation analysis, primitive discovery, and exploit development.
license: MIT
compatibility: opencode
---

# CTF Pwn

## What I do

- Inspect binaries and libraries.
- Identify protections such as NX, PIE, RELRO, canary, and ASLR assumptions.
- Find the bug class and turn it into a reliable primitive.
- Build local and remote pwntools exploits.

## When to use me

Use this for ELF or PE challenges, remote socket services, shellcode tasks, or memory corruption problems.

## Workflow

1. Triage with `file`, `checksec`, `strings`, and a quick run if safe.
2. Determine architecture, linking, protections, and I/O behavior.
3. Identify the vulnerability class.
4. Prove control with the smallest possible primitive.
5. Only then build the full exploit path to leak, calculate bases, and get code execution or flag access.

## Parallel lanes

Binary exploitation often presents multiple bug classes or leak paths. Run parallel reconnaissance lanes when safe:
- Lane A: Static analysis for obvious overflows, format strings, or UAF patterns.
- Lane B: Dynamic analysis for I/O behavior, crash sites, and interaction flow.
- Lane C: Leak primitive discovery (format string, info leak bugs, predictable addresses).
- Lane D: ROP gadget or one-gadget feasibility check for the target libc/runtime.
Merge when one lane confirms a reachable vulnerability and a viable primitive; abandon lanes that require impossible preconditions (e.g., full RELRO for GOT overwrite attempts).

## Common exploit paths

- Stack overflow to ROP.
- Format string to leaks and writes.
- Heap corruption to allocator abuse.
- Logic bugs leading to arbitrary read or write.
- Bad sandbox assumptions or command execution paths.

## Rules

- Separate facts from assumptions about offsets and addresses.
- Verify each primitive locally before composing the full chain.
- Use scripts instead of manual steps once interaction gets non-trivial.
- Keep libc and loader versions next to the challenge files when relevant.
