#!/usr/bin/env python3
"""Copy the bundled picture into the output folder.

The script looks for entry.png sitting next to itself, then
writes an identical copy to /output/entry.png so the judging
harness can pick it up. Everything is deterministic: no
timestamps, no randomness, no network access.
"""

import os
import shutil
import sys

MAX_BYTES = 1_048_576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def check_picture(path):
    """Reject empty, oversized, or non-image input early."""
    size = os.path.getsize(path)
    if size == 0:
        raise ValueError("entry.png is empty")
    if size > MAX_BYTES:
        raise ValueError("entry.png exceeds the 1 MiB limit")
    with open(path, "rb") as fh:
        head = fh.read(8)
    if not (head.startswith(PNG_MAGIC) or head.startswith(JPEG_MAGIC)):
        raise ValueError("entry.png is not a PNG or JPEG image")
    return size


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        print("entry.png not found next to script", file=sys.stderr)
        return 1
    try:
        check_picture(source)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, dest)

    try:
        os.chmod(dest, 0o644)
    except OSError:
        pass
    try:
        os.chmod(out_dir, 0o755)
    except OSError:
        pass

    print("wrote", dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
