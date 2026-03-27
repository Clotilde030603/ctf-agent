#!/usr/bin/env python3

import os
from collections.abc import Callable, Iterable, Iterator
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from typing import Optional, TypeVar


T = TypeVar("T")
R = TypeVar("R")

GLOBAL_WORKER_ENV = "CTF_PARALLEL_WORKERS"
GLOBAL_CAP_ENV = "CTF_PARALLEL_CAP"


def _positive_env(name: Optional[str]) -> Optional[int]:
    if not name:
        return None
    raw_value = os.environ.get(name)
    if raw_value is None:
        return None
    try:
        value = int(raw_value)
    except ValueError:
        return None
    return value if value >= 1 else None


def clamp_workers(requested: int, *, minimum: int = 1, cap: int = 32) -> int:
    return max(minimum, min(requested, cap))


def auto_workers(
    task_count: Optional[int] = None,
    *,
    cpu_multiplier: int = 4,
    minimum: int = 4,
    cap: int = 32,
) -> int:
    auto_count = clamp_workers((os.cpu_count() or 1) * cpu_multiplier, minimum=minimum, cap=cap)
    if task_count is not None:
        auto_count = min(auto_count, max(1, task_count))
    return auto_count


def resolve_workers(
    requested: Optional[int] = None,
    *,
    task_count: Optional[int] = None,
    default: Optional[int] = None,
    env_var: Optional[str] = None,
    global_env: Optional[str] = GLOBAL_WORKER_ENV,
    cap: int = 32,
    cap_env: Optional[str] = GLOBAL_CAP_ENV,
    minimum: int = 1,
    auto_minimum: int = 4,
    auto_multiplier: int = 4,
) -> int:
    resolved_cap = _positive_env(cap_env) or cap
    target = requested
    if target is None:
        target = _positive_env(env_var)
    if target is None:
        target = _positive_env(global_env)
    if target is None:
        if default is None:
            return auto_workers(
                task_count,
                cpu_multiplier=auto_multiplier,
                minimum=max(minimum, auto_minimum),
                cap=resolved_cap,
            )
        target = default
    target = clamp_workers(target, minimum=minimum, cap=resolved_cap)
    if task_count is not None:
        target = min(target, max(1, task_count))
    return target


def _submit_next(
    executor: ThreadPoolExecutor,
    pending: dict[Future[R], T],
    items: Iterator[T],
    fn: Callable[[T], R],
) -> bool:
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
    max_workers = clamp_workers(workers, cap=cap)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        pending: dict[Future[R], T] = {}
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
    max_workers = clamp_workers(workers, cap=cap)
    executor = ThreadPoolExecutor(max_workers=max_workers)
    should_wait_for_shutdown = True
    try:
        pending: dict[Future[R], T] = {}
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
                    should_wait_for_shutdown = False
                    executor.shutdown(wait=False, cancel_futures=True)
                    return item, result
                _submit_next(executor, pending, iterator, fn)
    finally:
        if should_wait_for_shutdown:
            executor.shutdown(wait=True, cancel_futures=True)
    return None


__all__ = [
    "GLOBAL_CAP_ENV",
    "GLOBAL_WORKER_ENV",
    "auto_workers",
    "clamp_workers",
    "parallel_first",
    "parallel_unordered",
    "resolve_workers",
]
