#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys
from typing import Optional


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ctf_parallel import parallel_first, resolve_workers



def load_lines(path: str) -> list[str]:
    file = Path(path)
    if not file.exists():
        return []
    return [line.strip() for line in file.read_text(encoding="utf-8").splitlines() if line.strip()]


def try_one(candidate: str) -> Optional[str]:
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Parallel CTF solve skeleton")
    parser.add_argument("input", nargs="?", default="candidates.txt")
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=None,
        help="worker threads (default: 16; env: CTF_SOLVER_WORKERS or CTF_PARALLEL_WORKERS)",
    )
    args = parser.parse_args()

    candidates = load_lines(args.input)
    if not candidates:
        print(f"add work items to {args.input}")
        return

    worker_count = resolve_workers(
        args.workers,
        task_count=len(candidates),
        default=16,
        env_var="CTF_SOLVER_WORKERS",
        cap=32,
    )
    hit = parallel_first(candidates, try_one, workers=worker_count, cap=32)
    if hit is None:
        print(f"checked {len(candidates)} items without a hit")
        return

    candidate, result = hit
    print(candidate)
    print(result)


if __name__ == "__main__":
    main()
