# Clinical tier: public-scope notice

This directory intentionally contains only a metadata manifest. The 67 case histories,
201 task/reference records, and 209 diagnostic images are not distributed in this
public-scope repository.

Deidentified per-evaluation numeric outputs are available in
`results/clinical/clinical_804_numeric_deidentified.csv`. They preserve the 67-case
clustering needed for descriptive and grouped analysis, while omitting case text,
diagnostic images, reference answers, raw model responses, adjudicator rationales,
source locators, and content fingerprints.

The withheld clinical materials remain outside the scope of this frozen public
release. This repository cannot be used to rerun clinical model inference from the
original inputs.
