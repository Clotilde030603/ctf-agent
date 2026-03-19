# Notes

## Timer

- Start time:
- Deadline:
- Current best lead: encoded-word subject injection + predictable MIME boundary + 2x admin bot trigger

## Facts

- Challenge title is `secure-email-service` and category is `Web Exploitation`.
- Live service endpoint was `http://activist-birds.picoctf.net:53447/`.
- `/api/password` gives the initial `user@ses` password once; current instance password used was `cf2599e7db6fc515458c9ee259da50ef`.
- The admin bot stores the real flag in `localStorage.flag`, logs in as `admin@ses`, opens the first inbox email, and replies to it.
- Signed HTML emails are rendered into `shadow.innerHTML` after client-side S/MIME verification.
- User mail is normally unsigned, but the admin reply path signs a new email whose subject is `Re: ${parsed.subject}`.
- Encoded-word syntax preserves newlines through the frontend parser, which lets the attacker inject malformed headers into the admin's reply subject.
- Python MIME boundaries are generated from predictable `random.randrange(sys.maxsize)` output.
- Predicting the admin boundary and injecting a UTF-7 HTML part makes the admin sign attacker-controlled HTML.
- Triggering the bot twice causes the admin to first send the malicious signed email to itself and then open it, executing XSS.
- The XSS used the admin token to call `/api/send` and mail `localStorage.flag` back to `user@ses`.
- The returned email body contained `picoCTF{always_a_step_ahead_fb2a1a8c}`.

## Hypotheses

- The intended solve is a parser differential plus boundary prediction chain, not a simple auth bypass.

## Disproved ideas

- Plain user HTML or plain XSS payloads do not render because unsigned HTML is rejected.
- Simple `\nHeader:` subject injection crashes email generation; the bypass requires `Header : value` formatting and encoded-word transport.

## Useful commands

- Collect boundaries by repeatedly sending mail to `user@ses` and extracting `===============(\d+)==` from raw MIME.
- Crack Python `random` state with `symbolic_mersenne_cracker` and predicted 63-bit boundary outputs.
- Trigger the bot twice with `POST /api/admin_bot`.

## Flag candidates

- `picoCTF{always_a_step_ahead_fb2a1a8c}`
