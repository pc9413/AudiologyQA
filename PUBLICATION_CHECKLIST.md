# Release record

## Completed release checks

- [x] Separate public-scope repository created without modifying the private master.
- [x] Educational and Research counts match the manuscript (6,314 total questions).
- [x] Research SA per-item labels match the reported 22.8%-30.0% accuracy range.
- [x] Clinical numeric derivative contains 804 unique case-model-task evaluations.
- [x] Clinical case text, images, references, model responses, rationales, reviewer
  identities, and unblinding keys are absent.
- [x] Reported clinical descriptive statistics reproduce from the numeric derivative.
- [x] Quality flags, schemas, prompts, explicit inventory, and checksums are included.
- [x] Clinical response hashes, private case-record hashes, and private-artifact
  fingerprints are excluded from the public scope.
- [x] Public release files pass the repository validation and checksum checks.
- [x] The release boundary is documented in the README and data-availability note.

## Final release state

- Version `1.0.0-public-scope` is the frozen public benchmark release corresponding
  to the JMIR R3 manuscript snapshot.
- Educational and Research questions and reference answers are released in full.
- Clinical publication is intentionally limited to metadata and deidentified numeric
  results; the original clinical materials are outside the public release scope.
- The MIT license applies only to newly written analysis code. Dataset-use boundaries
  are recorded in `DATA_RIGHTS.md`.

Current status: **released, validated, and frozen**.
