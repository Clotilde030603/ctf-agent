#!/usr/bin/env python3

from pathlib import Path


def load_input(path: str) -> bytes:
    return Path(path).read_bytes()


def main() -> None:
    data = load_input("ciphertext.bin")
    print(f"loaded {len(data)} bytes")
    # TODO: add challenge-specific decoding or attack logic.


if __name__ == "__main__":
    main()
