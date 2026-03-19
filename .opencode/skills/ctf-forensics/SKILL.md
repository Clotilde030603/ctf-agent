---
name: ctf-forensics
description: Solve forensics challenges by triaging artifacts, extracting embedded data, following metadata trails, and validating each finding.
license: MIT
compatibility: opencode
---

# CTF Forensics

## What I do

- Triage archives, disk images, pcaps, documents, images, audio, logs, and memory artifacts.
- Extract metadata and hidden content.
- Follow timelines, embedded payloads, and protocol traces.
- Turn discoveries into a clean evidence chain.

## When to use me

Use this for artifact-heavy challenges where the main task is locating, extracting, or reconstructing hidden information.

## Workflow

1. Identify file types and container layers.
2. Extract metadata and obvious embedded objects.
3. Inspect timestamps, authorship, paths, and protocol endpoints.
4. Carve, decode, or reconstruct the most suspicious artifacts.
5. Validate any flag candidate with context from the evidence trail.

## High-value checks

- `binwalk`, `exiftool`, `strings`, `file`, and hex views.
- Alternate streams, appended data, or malformed headers.
- PCAP credentials, file transfers, DNS clues, or covert channels.
- Document revision history and metadata.
- Steganography only after easier metadata and container checks are exhausted.

## Rules

- Keep original artifacts untouched.
- Record exactly how extracted files were obtained.
- Prefer reversible extraction steps.
- Treat timestamps carefully because they may be forged or transformed.
