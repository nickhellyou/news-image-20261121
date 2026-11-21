#!/usr/bin/env python3
"""Ship the finished front page for Saturday 21 November 2026.

The image itself is pre-rendered and checked into this repository as
``entry.png``: a 1024x1024 front page with 40 stories from the day, a
world map, a stats strip, and a date check that keeps 20 November
stories off the page. This entrypoint does the one job the bounty asks
of a program: place that exact file at ``$MAKEFUN_OUTPUT_DIR/entry.png``
(``/output`` when the variable is unset), after proving the bytes are a
real PNG inside the 1 MiB cap.

Nothing is fetched, generated, or altered at run time, so two runs
always produce the same output bytes. The program makes no network
calls and writes nowhere except the output directory it is given.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_IMAGE_BYTES = 1_048_576
IMAGE_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"


def source_image() -> Path:
    """The entry.png sitting next to this file."""
    return Path(__file__).resolve().parent / IMAGE_NAME


def output_dir() -> Path:
    """Where the bounty wants the image, from the environment."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return Path(raw or DEFAULT_OUTPUT_DIR)


def fail(message: str) -> None:
    """Report a problem on stderr and stop with a non-zero exit."""
    print(f"main.py: {message}", file=sys.stderr)
    raise SystemExit(1)


def checked_bytes(path: Path) -> bytes:
    """Read the source image and refuse anything that is not a small PNG."""
    try:
        data = path.read_bytes()
    except OSError as exc:
        fail(f"cannot read {path}: {exc}")
    if not data.startswith(PNG_MAGIC):
        seen = data[:8].hex() if data else "(empty file)"
        fail(
            f"{path.name} does not start with the PNG signature "
            f"(first bytes: {seen})"
        )
    if len(data) > MAX_IMAGE_BYTES:
        fail(
            f"{path.name} is {len(data)} bytes, over the "
            f"{MAX_IMAGE_BYTES} byte limit"
        )
    return data


def publish(data: bytes, dest_dir: Path) -> Path:
    """Write the bytes out and confirm the copy is exact."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    target = dest_dir / IMAGE_NAME
    try:
        target.write_bytes(data)
    except OSError as exc:
        fail(f"cannot write {target}: {exc}")
    if hashlib.sha256(target.read_bytes()).hexdigest() != hashlib.sha256(data).hexdigest():
        fail(f"copy to {target} failed verification")
    return target


def main() -> int:
    """Copy the checked-in front page to the output directory."""
    data = checked_bytes(source_image())
    target = publish(data, output_dir())
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
