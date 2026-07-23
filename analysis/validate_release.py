#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
errors = []
checks = []


def check(condition, message):
    checks.append(message)
    if not condition:
        errors.append(message)


def read_jsonl(relative):
    records = []
    with (ROOT / relative).open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                errors.append(f"{relative}:{line_number}: {exc}")
    return records


def read_csv(relative):
    with (ROOT / relative).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def as_bool(value):
    normalized = str(value).strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    raise ValueError(f"Invalid boolean value: {value!r}")


educational = read_jsonl("data/questions/educational_questions.jsonl")
research = read_jsonl("data/questions/research_questions.jsonl")
check(len(educational) == 3139, "Educational total is 3,139")
check(Counter(row["question_type"] for row in educational) == {"MCQ": 356, "TF": 1112, "FIB": 1671}, "Educational type counts match manuscript")
check(len({row["id"] for row in educational}) == 3139, "Educational IDs are unique")
check(len(research) == 3175, "Research total is 3,175")
check(Counter(row["question_type"] for row in research) == {"MCQ": 529, "TF": 1186, "SA": 1460}, "Research type counts match manuscript")
check(len({row["id"] for row in research}) == 3175, "Research IDs are unique")

manifest = read_csv("data/clinical/clinical_case_manifest.csv")
check(len(manifest) == 67, "Clinical metadata manifest has 67 cases")
check(sum(int(row["number_of_tasks"]) for row in manifest) == 201, "Clinical metadata manifest references 201 tasks")
check(sum(int(row["number_of_images"]) for row in manifest) == 209, "Clinical metadata manifest references 209 withheld images")
check("private_case_record_sha256" not in manifest[0], "Clinical manifest contains no private-record hash")
check(not (ROOT / "data/clinical_cases.jsonl").exists(), "No clinical case JSONL is present")
check(not (ROOT / "data/clinical_images").exists(), "No clinical image directory is present")

clinical = read_csv("results/clinical/clinical_804_numeric_deidentified.csv")
allowed_clinical_columns = {
    "evaluation_id", "case_id", "model", "question_type", "numerical_accuracy",
    "test_coverage", "description_accuracy", "hallucination_free", "diagnostic_accuracy",
    "reasoning_logic", "evidence_support", "relevance_to_diagnosis", "clinical_feasibility",
    "completeness", "weighted_score", "final_score", "grade", "critical_error_flag",
    "critical_error_categories", "score_capped", "passed",
}
check(len(clinical) == 804, "Clinical numeric result has 804 rows")
check(set(clinical[0]) == allowed_clinical_columns, "Clinical numeric result uses only approved columns")
check("response_sha256" not in clinical[0], "Clinical numeric result contains no response fingerprint")
check(len({row["evaluation_id"] for row in clinical}) == 804, "Clinical evaluation IDs are unique")
check(len({(row["case_id"], row["model"], row["question_type"]) for row in clinical}) == 804, "Clinical case-model-task combinations are unique")
check(Counter(row["question_type"] for row in clinical) == {"Q1": 268, "Q2": 268, "Q3": 268}, "Clinical question-type counts are 268 each")
check(len({row["case_id"] for row in clinical}) == 67, "Clinical result retains 67 pseudonymous case clusters")
check(len({row["model"] for row in clinical}) == 4, "Clinical result contains four models")
check(sum(as_bool(row["passed"]) for row in clinical) == 684, "Clinical pass numerator is 684")
check(sum(as_bool(row["critical_error_flag"]) for row in clinical) == 105, "Clinical any-critical-error numerator is 105")
check(abs(statistics.mean(float(row["final_score"]) for row in clinical) - 75.1374) < 0.001, "Clinical mean reproduces 75.1374")
check(Counter(row["grade"] for row in clinical) == {"A": 231, "B": 237, "C": 216, "D": 120}, "Clinical grade distribution matches the manuscript")

def expected_frozen_grade(row):
    score = float(row["final_score"])
    if score > 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 50:
        return "C"
    if score >= 25:
        return "D"
    return "F"

check(all(row["grade"] == expected_frozen_grade(row) for row in clinical), "Clinical grades follow the disclosed frozen >90 A boundary")
check(sum(float(row["final_score"]) == 90.0 and row["grade"] == "B" for row in clinical) == 43, "Exactly 43 frozen rows disclose the 90-point B boundary")

sa = read_csv("results/research/sa_item_results.csv")
research_sa_ids = {row["id"] for row in research if row["question_type"] == "SA"}
check(len(sa) == 1460, "Research SA result has 1,460 rows")
check({row["research_item_id"] for row in sa} == research_sa_ids, "Research SA result IDs exactly match SA question IDs")
expected_sa = {
    "gemini_2_5_pro_correct": 438,
    "grok_4_correct": 394,
    "openai_o3_correct": 349,
    "claude_sonnet_4_thinking_correct": 333,
}
for field, expected in expected_sa.items():
    check(sum(int(row[field]) for row in sa) == expected, f"{field} numerator is {expected}")

fidelity = read_csv("results/research/reference_fidelity_labels.csv")
check(len(fidelity) == 210, "Reference-fidelity audit has 210 labels")
check(Counter(row["human_reference_fidelity_label"] for row in fidelity) == {"Accurate": 209, "Defensible": 1}, "Reference-fidelity labels are 209 Accurate and 1 Defensible")

sources = read_csv("metadata/sources.csv")
check(all(row["tier"] in {"educational", "research"} for row in sources), "Source registry contains no clinical sources")
flags = read_csv("metadata/item_quality_flags.csv")
check(all(row["record_id"].startswith(("EDU-", "RES-")) for row in flags), "Quality flags contain no clinical records")

all_files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
check(not any("unblinding" in path.name.lower() or path.name.lower() == "clinical_cases.jsonl" for path in all_files), "No unblinding key or clinical-case data file is present")
check(not any(path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".tif", ".tiff", ".webp", ".dcm", ".dicom", ".pdf"} for path in all_files), "No image, DICOM, or PDF asset is present")

inventory_path = ROOT / "metadata/release_inventory.txt"
inventory = {line for line in inventory_path.read_text(encoding="utf-8").splitlines() if line}
actual_inventory = {path.relative_to(ROOT).as_posix() for path in all_files}
check(actual_inventory == inventory, "Repository contents exactly match the explicit public release inventory")

for path in all_files:
    if path.suffix.lower() not in {".md", ".json", ".jsonl", ".csv", ".py", ".txt", ".cff", ""}:
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    local_home_marker = "/" + "Users" + "/" + "pc9413"
    if local_home_marker in text:
        errors.append(f"Local absolute path leaked in {path.relative_to(ROOT)}")

report = {
    "status": "passed" if not errors else "failed",
    "checks_run": len(checks),
    "errors": errors,
    "counts": {"educational": len(educational), "research": len(research), "clinical_numeric": len(clinical), "research_sa_results": len(sa)},
}

parser = argparse.ArgumentParser()
parser.add_argument("--write-report", action="store_true")
args = parser.parse_args()
if args.write_report:
    (ROOT / "metadata/validation_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

print(json.dumps(report, indent=2))
raise SystemExit(0 if not errors else 1)
