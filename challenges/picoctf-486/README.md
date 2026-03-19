# picoctf-486

- Category guess: `pwn`
- Workflow hint: Start with ctf-orchestrator, then likely route into ctf-pwn.
- Challenge title: `handoff`

## Prompt

Exploit the remote binary using a negative index bug in the message path to place shellcode in memory and redirect execution with a `jmp rax` ret2reg gadget.
