# Notes

## Timer

- Start time:
- Deadline:
- Current best lead: inspect PDF metadata, especially author/producer fields

## Facts

- Public writeup for challenge 530 identifies the challenge as `Riddle Registry` in the forensics category.
- The provided artifact is a PDF named `confidential.pdf`.
- Running `exiftool confidential.pdf` or inspecting the raw PDF metadata reveals `Author : cGljb0NURntwdXp6bDNkX20zdGFkYXRhX2YwdW5kIV9lZTQ1NDk1MH0=`.
- The `Author` field value is Base64.
- Decoding the Base64 string yields `picoCTF{puzzl3d_m3tadata_f0und!_ee454950}`.

## Hypotheses

- The challenge is designed to test metadata inspection rather than visible PDF content extraction.

## Disproved ideas

- Plain `strings confidential.pdf | grep picoCTF` is not enough because the flag is not stored as raw visible text.

## Useful commands

- `exiftool confidential.pdf`
- `echo "cGljb0NURntwdXp6bDNkX20zdGFkYXRhX2YwdW5kIV9lZTQ1NDk1MH0=" | base64 -d`

## Flag candidates

- `picoCTF{puzzl3d_m3tadata_f0und!_ee454950}`
