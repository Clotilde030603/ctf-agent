#!/usr/bin/env python3

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Optional


TEXT_EXTENSIONS = {
    ".txt",
    ".md",
    ".py",
    ".js",
    ".ts",
    ".json",
    ".yaml",
    ".yml",
    ".html",
    ".css",
    ".xml",
    ".csv",
    ".php",
    ".c",
    ".cpp",
    ".rs",
    ".go",
    ".java",
    ".sh",
}

MAX_TEXT_PREVIEW = 12


def run_command(command: list[str], cwd: Optional[Path] = None) -> str:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        return f"error: {exc}"
    output = result.stdout.strip() or result.stderr.strip()
    return output[:1200] if output else ""


def available(command: str) -> bool:
    return shutil.which(command) is not None


def file_type(path: Path) -> str:
    if available("file"):
        output = run_command(["file", "-b", str(path)])
        if output:
            return output
    if path.is_dir():
        return "directory"
    return "unknown"


def maybe_preview_text(path: Path) -> list[str]:
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    return lines[:MAX_TEXT_PREVIEW]


def infer_category(entries: list[dict[str, object]]) -> str:
    haystack = " ".join(
        f"{entry['path']} {entry.get('type', '')}"
        for entry in entries
    ).lower()
    if any(token in haystack for token in ["http", "html", "php", "javascript", "flask", "node.js"]):
        return "web"
    if any(token in haystack for token in ["elf", "shared object", "pie executable", "64-bit lsb"]):
        return "pwn or rev"
    if any(token in haystack for token in ["pcap", "png", "jpeg", "zip archive", "pdf document", "audio"]):
        return "forensics"
    if any(token in haystack for token in ["cipher", "base64", "hex", "rsa", "aes"]):
        return "crypto"
    return "misc"


def collect_entry(path: Path) -> dict[str, object]:
    entry: dict[str, object] = {
        "path": str(path),
        "name": path.name,
        "is_dir": path.is_dir(),
    }
    if path.is_file():
        entry["size"] = path.stat().st_size
        entry["type"] = file_type(path)
        entry["preview"] = maybe_preview_text(path)

        if available("strings") and path.stat().st_size <= 2_000_000:
            strings_output = run_command(["strings", "-n", "6", str(path)])
            if strings_output:
                entry["strings_sample"] = strings_output.splitlines()[:20]

        if available("checksec") and path.suffix == "" and "ELF" in str(entry.get("type", "")):
            checksec_output = run_command(["checksec", "--file", str(path)])
            if checksec_output:
                entry["checksec"] = checksec_output
    else:
        entry["type"] = "directory"
    return entry


def main() -> None:
    parser = argparse.ArgumentParser(description="Quick triage for a CTF challenge directory")
    parser.add_argument("target", help="challenge directory or file")
    parser.add_argument(
        "--output",
        default="triage.json",
        help="output file name inside the target directory when target is a directory",
    )
    args = parser.parse_args()

    target = Path(args.target)
    if not target.exists():
        raise SystemExit(f"target does not exist: {target}")

    paths = [target] if target.is_file() else sorted(target.iterdir())
    entries = [collect_entry(path) for path in paths]

    report = {
        "target": str(target),
        "entry_count": len(entries),
        "likely_category": infer_category(entries),
        "entries": entries,
        "next_actions": [
            "Load ctf-orchestrator and review this triage report first.",
            "Promote the most likely category into a specialist skill.",
            "Convert findings into notes.md facts and hypotheses.",
        ],
    }

    rendered = json.dumps(report, indent=2)
    print(rendered)

    if target.is_dir():
        output_path = target / args.output
        output_path.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
