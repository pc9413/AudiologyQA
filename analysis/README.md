# Analysis

- `validate_release.py` checks counts, IDs, allowed fields, scope, and privacy guards.
- `reproduce_descriptive_results.py` recomputes the main descriptive results and
  reviewer-agreement statistics from public files.
- `profile_data_quality.py` regenerates the question-pool quality profile.
- `generate_checksums.py` regenerates SHA-256 values only for the explicit files in
  `metadata/release_inventory.txt`; ignored or unexpected files are never hashed.
- `verify_checksums.py` verifies the release manifest.

All scripts use the Python standard library and can be run from any working directory.
