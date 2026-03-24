#!/usr/bin/env python3

import argparse
from collections.abc import Callable, Iterable, Iterator
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path
from typing import Optional, TypeVar


T = TypeVar("T")
R = TypeVar("R")


def load_lines(path: str) -> list[str]:
    file = Path(path)
    if not file.exists():
        return []
    return [line.strip() for line in file.read_text(encoding="utf-8").splitlines() if line.strip()]


def bounded_workers(requested: int = 16, cap: int = 32) -> int:
    return max(1, min(requested, cap))


def _submit_next(executor, pending: dict, items: Iterator[T], fn: Callable[[T], R]) -> bool:
    try:
        item = next(items)
    except StopIteration:
        return False
    pending[executor.submit(fn, item)] = item
    return True


def parallel_unordered(
    items: Iterable[T],
    fn: Callable[[T], R],
    *,
    workers: int = 16,
    cap: int = 32,
) -> Iterator[tuple[T, R]]:
    iterator = iter(items)
    max_workers = bounded_workers(workers, cap)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        pending: dict = {}
        while len(pending) < max_workers and _submit_next(executor, pending, iterator, fn):
            pass
        while pending:
            done, _ = wait(pending, return_when=FIRST_COMPLETED)
            for future in done:
                item = pending.pop(future)
                yield item, future.result()
                _submit_next(executor, pending, iterator, fn)


def parallel_first(
    items: Iterable[T],
    fn: Callable[[T], R],
    *,
    workers: int = 16,
    cap: int = 32,
) -> Optional[tuple[T, R]]:
    iterator = iter(items)
    max_workers = bounded_workers(workers, cap)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        pending: dict = {}
        while len(pending) < max_workers and _submit_next(executor, pending, iterator, fn):
            pass
        while pending:
            done, _ = wait(pending, return_when=FIRST_COMPLETED)
            for future in done:
                item = pending.pop(future)
                result = future.result()
                if result is not None and result is not False:
                    for other in pending:
                        other.cancel()
                    return item, result
                _submit_next(executor, pending, iterator, fn)
    return None


def try_one(candidate: str) -> Optional[str]:
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Parallel CTF solve skeleton")
    parser.add_argument("input", nargs="?", default="candidates.txt")
    parser.add_argument("-w", "--workers", type=int, default=16)
    args = parser.parse_args()

    candidates = load_lines(args.input)
    if not candidates:
        print(f"add work items to {args.input}")
        return

    hit = parallel_first(candidates, try_one, workers=args.workers)
    if hit is None:
        print(f"checked {len(candidates)} items without a hit")
        return

    candidate, result = hit
    print(candidate)
    print(result)


if __name__ == "__main__":
    main()
