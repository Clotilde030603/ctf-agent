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

### Lane definitions
- Lane A: Static analysis for obvious overflows, format strings, or UAF patterns.
- Lane B: Dynamic analysis for I/O behavior, crash sites, and interaction flow.
- Lane C: Leak primitive discovery (format string, info leak bugs, predictable addresses).
- Lane D: ROP gadget or one-gadget feasibility check for the target libc/runtime.

### Lane budgets
- Maximum 3 lanes concurrently.
- 5 minutes per lane before requiring concrete findings.
- Static analysis (Lane A) gets priority if binary is small (<100KB).

### Merge criteria (primitive-driven)
- Confirmed crash/controllable fault (e.g., SEGV at user-controlled address).
- Working leak primitive (address exposure verified).
- Write primitive confirmed (can modify GOT, heap metadata, or stack).
- ROP chain or one-gadget feasible with available gadgets.

### Kill criteria
- Full RELRO confirmed and lane requires GOT overwrite.
- PIE + no leak primitive available after 10+ attempts.
- Canary enabled and no format string/stack leak found.
- Another lane has merged with working primitive.

### Automation triggers
- 3+ iterations of crash testing with different inputs.
- Format string offset hunting.
- ROP gadget enumeration.
- Heap manipulation sequences (allocate/free cycles).
- Any interactive service requiring repeated connections.

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
