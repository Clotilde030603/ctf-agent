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

## Parallel lanes

Crypto challenges often present multiple attack paths with varying cost. Run parallel hypothesis lanes:

### Lane definitions
- Lane A: Encoding and simple transform checks (base64, hex, XOR with short/repeated key, ROT).
- Lane B: Statistical and frequency analysis for classical ciphers or weak randomness.
- Lane C: Mathematical structure tests (small RSA exponent, shared factors, linear congruential generators).
- Lane D: Oracle behavior probing if any service interaction is available (padding oracles, error leaks).

### Lane budgets and search space limits
- Maximum 3 lanes concurrently.
- Lane A: 2-3 minutes (fast transforms only).
- Lane B: 5 minutes or until statistical anomaly found.
- Lane C: 10 minutes max; abandon if no algebraic structure emerges.
- Lane D: 20 queries max to oracle before requiring evidence of leak.

### Merge criteria
- Partial plaintext recovered (even 10+ characters).
- Key material or private parameters recovered.
- Oracle behavior confirms leak (distinct responses to crafted input).
- Mathematical weakness confirmed (shared factor, small exponent, predictable RNG).

### Kill criteria
- Search space exceeds feasible bounds (>2^30 operations without GPU/cluster).
- 50+ decryption attempts with no structure emerging.
- Oracle returns identical responses to 20+ distinct probes.
- Another lane has recovered partial plaintext.

### Automation triggers
- Brute force search of key space (XOR keys, small RSA factors).
- Batch decryption of multiple ciphertexts.
- Oracle query automation (padding oracle, error oracle).
- Mathematical computation (GCD, factorization, lattice reduction).

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
