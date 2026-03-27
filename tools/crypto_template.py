#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys
from typing import Optional, Union


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ctf_parallel import parallel_first, resolve_workers



def load_input(path: str) -> bytes:
    return Path(path).read_bytes()


def load_lines(path: str) -> list[str]:
    file = Path(path)
    if not file.exists():
        return []
    return [line.strip() for line in file.read_text(encoding="utf-8").splitlines() if line.strip()]


def try_key(candidate: str, data: bytes) -> Optional[Union[str, bytes]]:
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Parallel crypto solve skeleton")
    parser.add_argument("input", nargs="?", default="ciphertext.bin")
    parser.add_argument("-k", "--keys", default="keys.txt")
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=None,
        help="worker threads (default: 16; env: CTF_CRYPTO_WORKERS or CTF_PARALLEL_WORKERS)",
    )
    args = parser.parse_args()

    data = load_input(args.input)
    keys = load_lines(args.keys)
    if not keys:
        print(f"loaded {len(data)} bytes; add candidate keys to {args.keys}")
        return

    worker_count = resolve_workers(
        args.workers,
        task_count=len(keys),
        default=16,
        env_var="CTF_CRYPTO_WORKERS",
        cap=32,
    )
    hit = parallel_first(keys, lambda key: try_key(key, data), workers=worker_count, cap=32)
    if hit is None:
        print(f"checked {len(keys)} keys without a hit")
        return

    key, result = hit
    print(key)
    print(result)


if __name__ == "__main__":
    main()
