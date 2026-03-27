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

## Parallel lanes

Forensics artifacts often contain data at multiple layers. Run parallel extraction lanes when safe:

### Lane definitions
- Lane A: Metadata and container analysis (exiftool, binwalk, file signatures).
- Lane B: String and pattern extraction for credentials, URLs, or flag formats.
- Lane C: Timeline and correlation analysis for logs, pcaps, or revision histories.
- Lane D: Deep carving and steganography checks on high-entropy regions or suspicious media.

### Lane budgets and extraction layer limits
- Maximum 3 lanes concurrently.
- Lane A: 3 minutes (fast metadata pass).
- Lane B: 2 minutes for initial string extraction.
- Lane C: 5 minutes for timeline construction.
- Lane D: 10 minutes max; stego is last resort.
- Maximum 3 extraction layers deep (file → container → embedded → carved).

### Merge criteria
- Recoverable payload extracted (executable, compressed data, another file).
- Flag fragment or complete flag found.
- Credentials, keys, or URLs discovered.
- Timeline reveals anomalous event sequence.

### Kill criteria (noise thresholds)
- Lane returns only random/high-entropy data after initial extraction.
- 100+ strings scanned with no flag-like patterns or credentials.
- Timeline shows no anomalies after full correlation.
- Stego analysis produces no statistical anomalies after 10 minutes.
- Another lane has successfully extracted a payload.

### Layer exhaustion limits
- Stop at layer 3 if no new containers emerge (e.g., file → zip → inner file → nothing new).
- If binwalk finds 5+ false positives, abandon automated carving and switch to targeted extraction.

### Automation triggers
- Bulk string extraction with pattern matching.
- Batch file type identification.
- Automated timeline parsing (logs, pcaps).
- Steganography tool batch processing.

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
