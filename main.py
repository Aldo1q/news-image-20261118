#!/usr/bin/env python3
"""Entry for the make.fun bounty news-image-20261118.

Writes the 18 November 2026 world-news summary image to /output/entry.png.
Deterministic: copies the image shipped in this repository. No network.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"


def main():
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, DST)
    print(f"wrote {DST} ({os.path.getsize(DST)} bytes)")


if __name__ == "__main__":
    main()
