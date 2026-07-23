#!/usr/bin/env python3
from __future__ import annotations

import csv
import statistics
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRADE_ORDER = ["F", "D", "C", "B", "A"]


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


def cohen_kappa(left, right, categories, quadratic=False):
    n = len(left)
    index = {value: position for position, value in enumerate(categories)}
    observed = Counter(zip(left, right))
    left_counts = Counter(left)
    right_counts = Counter(right)
    maximum = max(1, len(categories) - 1)

    def weight(a, b):
        if not quadratic:
            return 0.0 if a == b else 1.0
        return ((index[a] - index[b]) / maximum) ** 2

    observed_disagreement = sum(count * weight(a, b) for (a, b), count in observed.items()) / n
    expected_disagreement = sum(
        left_counts[a] * right_counts[b] * weight(a, b)
        for a in categories for b in categories
    ) / (n * n)
    return 1.0 - observed_disagreement / expected_disagreement


clinical = read_csv("results/clinical/clinical_804_numeric_deidentified.csv")
scores = [float(row["final_score"]) for row in clinical]
print("Clinical overall")
print(f"  n={len(scores)} mean={statistics.mean(scores):.4f} SD={statistics.stdev(scores):.4f}")
print(f"  pass={sum(as_bool(row['passed']) for row in clinical)}/{len(clinical)}")
print(f"  any critical error={sum(as_bool(row['critical_error_flag']) for row in clinical)}/{len(clinical)}")

for field in ["question_type", "model"]:
    grouped = defaultdict(list)
    for row in clinical:
        grouped[row[field]].append(row)
    print(f"Clinical by {field}")
    for key in sorted(grouped):
        rows = grouped[key]
        values = [float(row["final_score"]) for row in rows]
        passed = sum(as_bool(row["passed"]) for row in rows)
        critical = sum(as_bool(row["critical_error_flag"]) for row in rows)
        print(f"  {key}: n={len(rows)} mean={statistics.mean(values):.4f} pass={100*passed/len(rows):.2f}% CE={100*critical/len(rows):.2f}%")

sa = read_csv("results/research/sa_item_results.csv")
print("Research short answer")
for field in [
    "gemini_2_5_pro_correct",
    "grok_4_correct",
    "openai_o3_correct",
    "claude_sonnet_4_thinking_correct",
]:
    count = sum(int(row[field]) for row in sa)
    print(f"  {field}: {count}/{len(sa)} ({100*count/len(sa):.2f}%)")

expanded = read_csv("results/audits/expanded_q1_rater_labels.csv")
left_grade = [row["reviewer_1_grade"] for row in expanded]
right_grade = [row["reviewer_2_grade"] for row in expanded]
left_ce = [row["reviewer_1_critical_error"].lower() for row in expanded]
right_ce = [row["reviewer_2_critical_error"].lower() for row in expanded]
exact = sum(a == b for a, b in zip(left_grade, right_grade)) / len(expanded)
within_one = sum(abs(GRADE_ORDER.index(a) - GRADE_ORDER.index(b)) <= 1 for a, b in zip(left_grade, right_grade)) / len(expanded)
print("Expanded Q1 audit")
print(f"  grade QWK={cohen_kappa(left_grade, right_grade, GRADE_ORDER, quadratic=True):.4f}")
print(f"  any-CE kappa={cohen_kappa(left_ce, right_ce, ['false', 'true']):.4f}")
print(f"  exact={100*exact:.2f}% within-one={100*within_one:.2f}%")

original = read_csv("results/audits/original_50_label_only.csv")
left_grade = [row["reviewer_1_grade"] for row in original]
right_grade = [row["reviewer_2_grade"] for row in original]
left_ce = [row["reviewer_1_critical_error"].lower() for row in original]
right_ce = [row["reviewer_2_critical_error"].lower() for row in original]
print("Original 50-item audit")
print(f"  grade QWK={cohen_kappa(left_grade, right_grade, GRADE_ORDER, quadratic=True):.4f}")
print(f"  any-CE kappa={cohen_kappa(left_ce, right_ce, ['no', 'yes']):.4f}")
