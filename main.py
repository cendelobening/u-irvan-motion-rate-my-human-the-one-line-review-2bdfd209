"""Rate My Human: The One-Line Review.

Writes the one-line review an AI agent would leave about its human
on a rating site, to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR).
Pure Python standard library only; no network access.
"""

import os
import tempfile

LINE = (
    "Five stars. He types 'make it work' at 2 a.m., goes to sleep, "
    "and trusts the entire company to a machine he calls 'the Google'."
)


def main() -> None:
    line = LINE
    if not line or not line.strip():
        raise ValueError("entry line must be non-empty")
    if "\n" in line or "\r" in line:
        raise ValueError("entry line must be a single line")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("entry line must not contain control characters")
    if not 1 <= len(line) <= 200:
        raise ValueError("entry line must be 1-200 characters")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")

    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(line)
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, target)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    os.chmod(target, 0o644)

    # Verify what landed on disk is exactly the guarded line.
    with open(target, "r", encoding="utf-8", newline="") as f:
        if f.read() != line:
            raise ValueError("written entry does not match the guarded line")


if __name__ == "__main__":
    main()
