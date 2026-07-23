# Clinical scoring rubric

Each dimension is rated from 1 (unacceptable) to 5 (excellent). The weighted
dimension score is transformed to a 0-100 scale as `(weighted_score - 1) * 25`.

| Task | Dimension | Weight |
|---|---|---:|
| Q1 | Numerical accuracy | 40% |
| Q1 | Test coverage | 30% |
| Q1 | Description accuracy | 20% |
| Q1 | Hallucination-free | 10% |
| Q2 | Diagnostic accuracy | 50% |
| Q2 | Reasoning logic | 30% |
| Q2 | Evidence support | 20% |
| Q3 | Relevance to diagnosis | 40% |
| Q3 | Clinical feasibility | 30% |
| Q3 | Completeness | 30% |

| Grade | Score | Meaning |
|---|---:|---|
| A | >90-100 in the frozen result file | Full correct |
| B | 75-90 in the frozen result file | Mostly correct |
| C | 50-74 | Partially correct |
| D | 25-49 | Mostly incorrect or capped for a non-dangerous critical error |
| F | 0-24 | Full wrong or capped for a dangerous recommendation |

Any critical error other than Dangerous Recommendation caps the score at 49
(maximum grade D). Dangerous Recommendation caps the score at 24 (maximum grade F).

## Frozen 90-point boundary

The manuscript rubric table describes A as 90-100 and B as 75-89, but the frozen
804-row operational result file assigns exactly 90.0 to B (43 uncapped rows) and
assigns A only above 90. This repository preserves those labels because they produce
the manuscript's reported grade distribution (A=231, B=237, C=216, D=120). Changing
the 43 labels would create a new analysis version and would no longer reproduce that
table. Consumers should use the disclosed frozen boundary for reproduction.
