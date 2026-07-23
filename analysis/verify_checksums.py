#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
manifest = ROOT / "metadata/checksums.sha256"
inventory = ROOT / "metadata/release_inventory.txt"
failures = []
checked = 0
manifest_paths = set()
for line in manifest.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    expected, relative = line.split("  ", 1)
    manifest_paths.add(relative)
    path = ROOT / relative
    if not path.is_file():
        failures.append(relative)
        continue
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    checked += 1
    if actual != expected:
        failures.append(relative)

expected_paths = {
    line for line in inventory.read_text(encoding="utf-8").splitlines()
    if line and line != "metadata/checksums.sha256"
}
if manifest_paths != expected_paths:
    failures.append("checksum_manifest_inventory_mismatch")

if failures:
    print(f"Checksum verification failed for {len(failures)} file(s):")
    for relative in failures:
        print(f"  {relative}")
    raise SystemExit(1)
print(f"Verified {checked} files successfully.")
