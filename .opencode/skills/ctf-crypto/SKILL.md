---
name: ctf-crypto
description: Solve cryptography challenges by fingerprinting the scheme, testing the weakest plausible attacks first, and scripting repeatable analysis.
license: MIT
compatibility: opencode
---

# CTF Crypto

## What I do

- Classify encodings, ciphers, hashes, and mathematical structures.
- Distinguish between textbook crypto and challenge-specific mistakes.
- Test attack hypotheses from cheapest to most likely.
- Write solver scripts for transformations, brute force, and algebraic recovery.

## When to use me

Use this for ciphertexts, keys, signatures, modular arithmetic, pseudorandomness challenges, and strange encoded blobs.

## Workflow

1. Establish what is encoding versus encryption versus hashing.
2. Record all known values, lengths, alphabets, and formatting clues.
3. Check for reused nonces, small exponents, weak randomness, oracle behavior, or structural leakage.
4. Script experiments so results are reproducible.
5. Confirm the recovered plaintext or flag format.

## High-value checks

- XOR with repeated or short keys.
- ECB or block-boundary leakage.
- RSA mistakes such as low exponent, bad padding, shared factors, or leaked structure.
- Linear congruential generator weaknesses.
- Custom schemes that are really simple transforms.

## Rules

- Do not call something RSA, AES, or ECC without evidence.
- Measure before brute forcing.
- Track byte lengths and endian assumptions carefully.
- When math is involved, state the exact model and variables before solving.
