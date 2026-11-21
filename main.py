#!/usr/bin/env python3
"""Stage the news-image entry for the make.fun harness.

The finished front page sits beside this script as ``entry.png``.  This
program copies a checked copy of it to the directory the harness reads,
taken from ``MAKEFUN_OUTPUT_DIR`` and defaulting to ``/output``.

Two guards run before the copy, so a damaged or oversized file can never
slip through by accident: the file has to open with the eight PNG magic
bytes, and it has to fit inside the 1 MiB cap.  After the copy, the
destination is hashed and compared with the source, so a partial write
is caught instead of reported as a success.
"""

import hashlib
import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1 * 1024 * 1024
SOURCE_NAME = "entry.png"


def fail(message):
    """Report an error and stop with a non-zero exit code."""
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def digest(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)

    if not os.path.isfile(source):
        fail(f"missing artwork: {source} not found")

    with open(source, "rb") as handle:
        data = handle.read()

    if not data.startswith(PNG_MAGIC):
        fail(f"{SOURCE_NAME} does not start with PNG magic bytes")
    if len(data) > MAX_BYTES:
        fail(f"{SOURCE_NAME} is {len(data)} bytes, over the 1 MiB limit")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, SOURCE_NAME)
    shutil.copyfile(source, target)

    if digest(target) != digest(source):
        fail(f"copy verification failed for {target}")

    print(f"wrote {target} ({len(data)} bytes, sha256 {digest(source)[:12]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
