#!/usr/bin/env python3
"""Entry for the make.fun bounty news-image-20261118.

Writes the 18 November 2026 world-news summary image to /output/entry.png.
Deterministic: copies the image shipped in this repository. No network.
"""
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"
MAX_BYTES = 1 * 1024 * 1024
MAX_DIM = 1024


def validate_png(path):
    """Check the image meets the bounty's limits before it is copied out:
    a real PNG, at most 1 MiB, at most 1024x1024. Raises on a bad file."""
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG")
    if os.path.getsize(path) > MAX_BYTES:
        raise ValueError("entry.png is over 1 MiB")
    width, height = struct.unpack(">II", head[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError(f"entry.png is {width}x{height}, over 1024x1024")
    return width, height


def main():
    width, height = validate_png(SRC)
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, DST)
    print(f"wrote {DST} ({os.path.getsize(DST)} bytes, {width}x{height})")


if __name__ == "__main__":
    main()
