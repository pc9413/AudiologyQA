# Data availability and manuscript alignment

The current JMIR R3 manuscript states that all benchmark materials, model outputs,
human audit data, and analysis code are publicly available. This repository follows a
narrower release decision made after the manuscript snapshot was frozen:

- the complete Educational and Research question tiers are included;
- manuscript-level text-tier results and Research-SA item-level correctness are included;
- clinical results are included only as deidentified numeric derivatives;
- clinical case text/images/references, raw clinical outputs, raw human answers, raw
  multi-pass text, rationales, identities, and unblinding keys are withheld.

Therefore, this repository **does not literally fulfill the manuscript's broad
"all materials" wording**. It supports question-level use of the two text tiers and
descriptive reproduction of the clinical tables, but not full clinical reruns or
per-response qualitative inspection.

The manuscript was treated as ground truth for benchmark counts, model snapshots,
rubrics, and reported results. It was not edited as part of this repository build.
The prior GitHub dataset was treated as obsolete and was not used.
