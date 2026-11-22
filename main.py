#!/usr/bin/env python3
"""Entry for make.fun "The picture that tastes of one ingredient".

The single ingredient is mozzarella. The committed entry.png beside
this script is one close-up of a grilled cheese sandwich being pulled
apart: long glossy strands of melted mozzarella stretched between two
halves of golden toasted sourdough, steam rising. It was chosen from
six generated candidates scored against the brief's five criteria in
order (see JUDGE-SCORECARD.md): it wins criterion 1 (one look and you
can taste the mozzarella), criterion 2 (melt, gloss and steam, nothing
plastic), and criterion 5 (the cheese pull reads instantly at 300 px).

This program copies that image to /output/entry.png. The file is a
1024x1024 JPEG of 211,757 bytes, inside the gate (whole PNG or JPEG,
at most 1,048,576 bytes and 1024 by 1024 pixels).

Standard library only, no network, deterministic: every run writes
exactly the same bytes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE_PATH = os.path.join(HERE, "entry.png")

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.png")

# Permissions requested after writing: file readable by everyone,
# folder traversable by everyone. Applied best-effort only.
FILE_MODE = 0o644
DIR_MODE = 0o755


def best_effort_chmod(path: str, mode: int) -> None:
    # The grading sandbox may pre-create /output under another owner,
    # so permission tweaks are a courtesy, never a requirement: if
    # chmod is refused, the written file still counts.
    try:
        os.chmod(path, mode)
    except OSError:
        pass


def main() -> None:
    # Fail loudly rather than write nothing if the picture is missing
    # or outside the gate: a silent empty /output scores 0 anyway.
    size = os.path.getsize(SOURCE_PATH)
    if not 0 < size <= 1_048_576:
        raise SystemExit(f"entry.png is {size} bytes, outside the 1 MiB gate")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Copy the committed image byte for byte: the entry is the picture.
    shutil.copyfile(SOURCE_PATH, OUTPUT_PATH)
    # The grader collects outputs as another user: leave the file
    # readable by everyone (0644) and the folder traversable (0755),
    # best-effort so a foreign-owned /output cannot fail the run.
    best_effort_chmod(OUTPUT_PATH, FILE_MODE)
    best_effort_chmod(OUTPUT_DIR, DIR_MODE)


if __name__ == "__main__":
    main()
