#!/usr/bin/env python3

import argparse
import os
import json
import stat
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
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
MAX_AUTO_WORKERS = 32


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


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return parsed


def detect_tools() -> dict[str, bool]:
    return {
        "file": available("file"),
        "strings": available("strings"),
        "checksec": available("checksec"),
    }


def default_worker_count(entry_count: int) -> int:
    if entry_count <= 1:
        return 1
    cpu_count = os.cpu_count() or 1
    return min(entry_count, max(4, min(MAX_AUTO_WORKERS, cpu_count * 4)))


def probe_worker_count(worker_count: int) -> int:
    return min(MAX_AUTO_WORKERS, max(2, worker_count * 2))


def file_type(path: Path, has_file_command: bool, is_dir: bool) -> str:
    if has_file_command:
        output = run_command(["file", "-b", str(path)])
        if output:
            return output
    if is_dir:
        return "directory"
    return "unknown"


def has_elf_magic(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            return handle.read(4) == b"\x7fELF"
    except OSError:
        return False


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


def collect_entry(
    path: Path,
    tools: dict[str, bool],
    probe_executor: Optional[ThreadPoolExecutor] = None,
) -> dict[str, object]:
    path_stat = path.stat()
    is_dir = stat.S_ISDIR(path_stat.st_mode)
    is_file = stat.S_ISREG(path_stat.st_mode)
    entry: dict[str, object] = {
        "path": str(path),
        "name": path.name,
        "is_dir": is_dir,
    }
    if is_file:
        size = path_stat.st_size
        preview = maybe_preview_text(path)
        likely_elf = path.suffix == "" and has_elf_magic(path)

        type_future = None
        strings_future = None
        checksec_future = None
        if probe_executor is not None:
            type_future = probe_executor.submit(file_type, path, tools["file"], is_dir)
            if tools["strings"] and size <= 2_000_000:
                strings_future = probe_executor.submit(run_command, ["strings", "-n", "6", str(path)])
            if tools["checksec"] and likely_elf:
                checksec_future = probe_executor.submit(run_command, ["checksec", "--file", str(path)])

        entry["size"] = size
        entry_type = (
            type_future.result()
            if type_future is not None
            else file_type(path, tools["file"], is_dir)
        )
        entry["type"] = entry_type
        entry["preview"] = preview

        if tools["strings"] and size <= 2_000_000:
            strings_output = (
                strings_future.result()
                if strings_future is not None
                else run_command(["strings", "-n", "6", str(path)])
            )
            if strings_output:
                entry["strings_sample"] = strings_output.splitlines()[:20]

        if tools["checksec"] and likely_elf and "ELF" in entry_type:
            checksec_output = (
                checksec_future.result()
                if checksec_future is not None
                else run_command(["checksec", "--file", str(path)])
            )
            if checksec_output:
                entry["checksec"] = checksec_output
    else:
        entry["type"] = "directory"
    return entry


def collect_entries(paths: list[Path], tools: dict[str, bool], worker_count: int) -> list[dict[str, object]]:
    probe_executor = None
    if any(tools.values()):
        probe_executor = ThreadPoolExecutor(
            max_workers=probe_worker_count(worker_count),
            thread_name_prefix="triage-probe",
        )

    def collect_with_probes(path: Path) -> dict[str, object]:
        return collect_entry(path, tools, probe_executor)

    if worker_count == 1:
        try:
            return [collect_with_probes(path) for path in paths]
        finally:
            if probe_executor is not None:
                probe_executor.shutdown(wait=True)

    try:
        with ThreadPoolExecutor(max_workers=worker_count, thread_name_prefix="triage") as executor:
            return list(executor.map(collect_with_probes, paths))
    finally:
        if probe_executor is not None:
            probe_executor.shutdown(wait=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Quick triage for a CTF challenge directory")
    parser.add_argument("target", help="challenge directory or file")
    parser.add_argument(
        "--output",
        default="triage.json",
        help="output file name inside the target directory when target is a directory",
    )
    parser.add_argument(
        "--workers",
        type=positive_int,
        default=None,
        help="number of worker threads to use for per-file analysis (default: auto)",
    )
    args = parser.parse_args()

    target = Path(args.target)
    if not target.exists():
        raise SystemExit(f"target does not exist: {target}")

    paths = [target] if target.is_file() else sorted(target.iterdir())
    tools = detect_tools()
    worker_count = args.workers or default_worker_count(len(paths))
    entries = collect_entries(paths, tools, worker_count)

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
