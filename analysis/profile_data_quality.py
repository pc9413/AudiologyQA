#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(relative: str) -> list[dict]:
    with (ROOT / relative).open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle]


def duplicate_summary(records: list[dict]) -> dict:
    full_keys = [
        (
            row["question_type"],
            row["question"],
            json.dumps(row.get("reference_answer"), sort_keys=True),
            json.dumps(row.get("options"), sort_keys=True),
        )
        for row in records
    ]
    stem_keys = [re.sub(r"\s+", " ", row["question"].strip().casefold()) for row in records]
    full_counts = Counter(full_keys)
    stem_counts = Counter(stem_keys)
    return {
        "exact_item_groups": sum(count > 1 for count in full_counts.values()),
        "rows_in_exact_item_groups": sum(count for count in full_counts.values() if count > 1),
        "duplicate_stem_groups": sum(count > 1 for count in stem_counts.values()),
        "rows_in_duplicate_stem_groups": sum(count for count in stem_counts.values() if count > 1),
    }


educational = read_jsonl("data/questions/educational_questions.jsonl")
research = read_jsonl("data/questions/research_questions.jsonl")
with (ROOT / "metadata/item_quality_flags.csv").open(encoding="utf-8", newline="") as handle:
    flags = list(csv.DictReader(handle))

report = {
    "status": "passed_with_disclosed_frozen_conditions",
    "educational": {
        "rows": len(educational),
        "unique_ids": len({row["id"] for row in educational}),
        "types": Counter(row["question_type"] for row in educational),
        "missing_difficulty": sum(row.get("difficulty") in {None, ""} for row in educational),
        "multiple_select_rows": sum(row.get("response_format") == "multiple_select" for row in educational),
        "duplicates": duplicate_summary(educational),
    },
    "research": {
        "rows": len(research),
        "unique_ids": len({row["id"] for row in research}),
        "types": Counter(row["question_type"] for row in research),
        "missing_difficulty": sum(row.get("difficulty") in {None, ""} for row in research),
        "duplicates": duplicate_summary(research),
    },
    "quality_flags": {
        "rows": len(flags),
        "by_flag": Counter(row["flag"] for row in flags),
    },
    "interpretation": [
        "Frozen exact duplicate items are retained for manuscript/result alignment.",
        "Stem-only duplication is reported separately because identical stems can differ in keyed answers or options.",
        "Missing difficulty labels are left null rather than inferred.",
        "Technical validation does not constitute source-rights clearance.",
    ],
}

# Convert Counter subclasses before serialization.
report["educational"]["types"] = dict(report["educational"]["types"])
report["research"]["types"] = dict(report["research"]["types"])
report["quality_flags"]["by_flag"] = dict(report["quality_flags"]["by_flag"])

output = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
(ROOT / "metadata/data_quality_report.json").write_text(output, encoding="utf-8")
print(output, end="")
