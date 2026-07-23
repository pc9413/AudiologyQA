# AUDIOLOGYBENCH

AUDIOLOGYBENCH is a three-tier benchmark for evaluating large language models in
clinical audiology. This repository contains the **frozen public release corresponding
to the JMIR R3 manuscript snapshot**. The manuscript itself was not changed.

## Release contents

| Component | Released content |
|---|---|
| Educational tier | All 3,139 questions and reference answers: 356 MCQ, 1,112 TF, 1,671 FIB |
| Research-derived tier | All 3,175 questions and reference answers: 529 MCQ, 1,186 TF, 1,460 SA |
| Educational/research results | Manuscript-reported model-by-format accuracy tables |
| Research SA results | 1,460 per-item binary correctness records for four models |
| Clinical results | 804 deidentified numeric evaluations across 67 cases, 4 models, and Q1-Q3 |
| Validation evidence | Label-only audit derivatives and reported statistical summaries |
| Methods | Prompts, rubrics, schemas, model snapshots, and reproducibility scripts |

The public question total is **6,314**. Research SA is included because it supports
the manuscript's central finding that short-answer evidence extraction remained the
most difficult research format.

## Release boundary

The 67 clinical case histories, 209 diagnostic images, 201 clinical reference-answer
records, raw clinical model responses, free-text adjudicator rationales, raw human
baseline answers, raw multi-pass text, reviewer identities, and unblinding keys are
not distributed. The clinical case manifest is metadata-only.

This design permits descriptive reproduction of the published clinical result tables,
but it does not permit rerunning the clinical model inference from the original case
inputs. See [DATA_AVAILABILITY_NOTE.md](DATA_AVAILABILITY_NOTE.md) for the exact scope.

## Repository map

- `data/questions/` — frozen Educational and Research question pools.
- `data/clinical/` — metadata-only clinical manifest.
- `results/` — aggregate results, SA per-item labels, deidentified clinical numeric
  results, and audit summaries.
- `prompts/` and `rubrics/` — evaluation instructions and scoring definitions.
- `analysis/` — standard-library validation and descriptive reproduction scripts.
- `metadata/` — source registry, model snapshots, quality flags, explicit public-file
  inventory, manifest, validation report, and checksums.

## Validate and reproduce

Run from the repository root:

```bash
python3 analysis/validate_release.py
python3 analysis/reproduce_descriptive_results.py
python3 analysis/profile_data_quality.py
python3 analysis/verify_checksums.py
```

No third-party Python packages are required.

## Release status

This is the completed and frozen public release corresponding to the JMIR R3
manuscript snapshot. Its question pools, reference answers, result files, prompts,
rubrics, schemas, and validation records define version `1.0.0-public-scope`.

The release scope is final: withheld clinical histories, images, reference records,
and raw response text are not part of this public benchmark. The MIT license applies
only to newly written analysis code. Dataset-use boundaries are documented in
[DATA_RIGHTS.md](DATA_RIGHTS.md), and the completed release record is documented in
[PUBLICATION_CHECKLIST.md](PUBLICATION_CHECKLIST.md).

## Citation

If you use AUDIOLOGYBENCH, please cite the accompanying manuscript. Machine-readable
citation metadata is available in [CITATION.cff](CITATION.cff).

This benchmark characterizes model capability; it does not certify clinical safety
and must not be used for patient care.
