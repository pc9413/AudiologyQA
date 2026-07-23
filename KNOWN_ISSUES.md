# Known issues

## Frozen question-pool conditions

- Educational exact duplicates: 29 groups / 58 rows (4 MCQ groups, 7 TF groups,
  18 FIB groups). They are preserved to maintain manuscript counts and result alignment.
- `EDU-MCQ-0331` has three keyed options and is multiple-select despite the broader
  single-best-answer description.
- Eleven educational records have semantic type/response-format mismatches; consumers
  should consult `response_format` and `metadata/item_quality_flags.csv`.
- Eleven educational difficulty labels are unresolved and remain null rather than
  being inferred.

## Result availability

- Per-item Educational model outputs were not found in the frozen local source set;
  model-by-format manuscript summaries are provided.
- Per-item Research MCQ/TF outputs were not found; manuscript summaries are provided.
- Research SA has complete per-item binary correctness labels, but raw answer text is
  omitted.
- Clinical numeric results are complete at 804 rows, but all original clinical text,
  images, references, responses, and rationales are omitted.
- The manuscript's rubric table labels 90 as grade A, whereas the frozen 804-row
  result file assigns exactly 90.0 to B (43 uncapped rows). Those labels are preserved
  to reproduce the manuscript grade distribution; see the clinical rubric note.

## Rights and attribution scope

Available source and bibliographic metadata are recorded in `metadata/sources.csv`.
Public access does not create a blanket license for third-party source materials; see
`DATA_RIGHTS.md` for the dataset-use boundary.
