# Notes

## Timer

- Start time:
- Deadline:
- Current best lead: option 2 with `choice = -1` and ret2reg via `jmp rax`

## Facts

- Challenge title is `handoff` and category is `Binary Exploitation`.
- Remote endpoint on this instance was `nc shape-facility.picoctf.net 52889`.
- Source exposes two stack overflows, but the practical solve is the message path with a negative recipient index.
- Public writeups and the real exploit path both use `choice = -1` in menu option 2.
- The binary is not stripped and contains a `jmp rax` gadget at `0x40116c`.
- A 48-byte payload of `shellcode.ljust(40, b"\x00") + p64(0x40116c)` is sufficient.
- Executing the shellcode spawns a shell on the remote service.
- After code execution, `pwd` returned `/app` and `ls` showed `flag.txt`, `handoff`, and `start.sh`.
- Reading `flag.txt` returned `picoCTF{p1v0ted_ftw_88e8cda3}`.

## Hypotheses

- The intended exploit is a ret2reg handoff: the vulnerable write path leaves a useful pointer in `rax`, and execution is redirected there.

## Disproved ideas

- The feedback overflow route was unnecessary for the real solve.
- Direct shellcode execution through the review field was the wrong path for this challenge.

## Useful commands

- `objdump -d handoff | grep -B1 -A1 'jmpq \*%rax'`
- `nc shape-facility.picoctf.net 52889`

## Flag candidates

- `picoCTF{p1v0ted_ftw_88e8cda3}`
