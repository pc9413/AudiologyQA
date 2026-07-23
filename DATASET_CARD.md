# Dataset card

## Purpose

AUDIOLOGYBENCH evaluates audiology knowledge, familiarity with research-derived
evidence, and multimodal clinical reasoning. Educational and research formats are
secondary descriptive endpoints; clinical rubric grades and critical-error rates are
the primary endpoint in the manuscript.

## Public data

- Educational: 3,139 objective items (356 MCQ, 1,112 TF, 1,671 FIB).
- Research-derived: 3,175 items (529 MCQ, 1,186 TF, 1,460 SA).
- Clinical: a 67-row metadata-only case manifest and 804 deidentified numeric result
  rows. Original case inputs are withheld.

Each public question retains its frozen benchmark ID, question type, response format,
reference answer, domain/difficulty metadata when available, and source identifier.

## Model panels

Eight models were evaluated on the Educational tier. Four frontier multimodal models
were evaluated on the Research and Clinical tiers. Exact snapshot identifiers are in
`metadata/model_run_manifest.csv`.

## Known limitations

- English-language materials are concentrated in US/Australian educational and
  clinical conventions.
- Some educational formats exhibit ceiling effects, especially web-style MCQ.
- Research TF is near ceiling; Research SA is the most discriminative text format.
- Gemini 2.5 Pro participated in generation/adjudication and was also evaluated on
  secondary tiers, creating a residual self-preference concern.
- Clinical per-item automated labels are imperfect; human audits support aggregate
  patterns more strongly than individual labels.
- The frozen clinical output uses B at exactly 90.0, despite the manuscript rubric
  table describing 90 as the lower bound of A; this boundary is disclosed and retained
  for reported grade-distribution alignment.
- The frozen educational pool contains disclosed duplicates, one multiple-select MCQ,
  semantic type mismatches, and 11 unresolved difficulty labels.
- Clinical cases may overlap model pretraining data; contamination was not formally
  excluded.
- The scoped public release cannot reproduce clinical inference without the withheld
  original case inputs.

## Intended use

Research benchmarking, error analysis, and reproducibility of reported descriptive
statistics. Not intended for diagnosis, treatment, patient-facing decision support,
or certification of model safety.
