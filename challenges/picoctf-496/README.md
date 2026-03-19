# picoctf-496

- Category guess: `web`
- Workflow hint: Start with ctf-orchestrator, then likely route into ctf-web.
- Challenge title: `secure-email-service`

## Prompt

Abuse S/MIME email handling so the admin bot signs attacker-controlled HTML and then executes XSS while viewing its own signed email. The final exfiltration path sends the admin's localStorage flag back to `user@ses` as a signed email.
