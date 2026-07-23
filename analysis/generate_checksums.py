#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "metadata/checksums.sha256"
INVENTORY = ROOT / "metadata/release_inventory.txt"
entries = []
for relative in INVENTORY.read_text(encoding="utf-8").splitlines():
    if not relative or relative == "metadata/checksums.sha256":
        continue
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"Inventory entry is missing or not a file: {relative}")
    entries.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {relative}")

OUTPUT.write_text("\n".join(entries) + "\n", encoding="utf-8")
print(f"Wrote checksums for {len(entries)} files.")
