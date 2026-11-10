# Changes

## November 10 2026 reproducibility audit

- Recovered candidate input was supplied locally; recorded SHA-256, schema, target codes, age scope and unresolved sample-selection provenance. Participant-level data remain outside the repository.
- Added a checksum-aware portable CLI and small reusable workflow module. Explicit category types, fold-local imputation/scaling, one-hot encoding and SMOTENC replace dtype-based categories and ordinary-SMOTE interpolation in the current recommended path.
- Compared 13 settings across three model families using training-only stratified CV. Added an always-negative reference, average precision and clearly qualified small-sample descriptive intervals.
- Completed an actual isolated-environment run and saved aggregate results separately from historical evidence. The reused holdout is explicitly retrospective.
- Added pinned reproduction dependencies and focused regression tests. Updated README, methods, findings, provenance, reproduction instructions and attribution.
- Marked the prior revised notebook as exploratory; its full execution, permutation and SHAP remain unverified. Preserved original notebook bytes, original figures and original result JSON.

## November 9 2026 portfolio review

- Replaced the template README with purpose, results, methods, tools, navigation, attribution and evidence limits.
- Added findings, methods/data dictionary, reproduction instructions and attribution documents.
- Preserved original notebook bytes in `notebooks/archive/Final_original.ipynb` and retained existing PNGs and commit history.
- Added machine-readable historical confusion matrices and a standard-library arithmetic audit; no retraining results invented.
- Corrected macro-F1 labeling and exposed positive-class F1 separately.
- Replaced silent data-loading failure with an explicit missing-file/schema check and portable root lookup.
- Corrected PAQ605 refused/unknown handling using the CDC codebook; these changes invalidate any claim that old results came from revised code.
- Fixed the SHAP explainer variable and used training data as its background; made SHAP optional.
- Specified balanced accuracy for permutation importance, fixed figure labeling/output location, and removed unsupported clinical/causal claims from the working notebook discussion.
- Removed the optional complexity calculation from the working run; it remains in the original.
- Cleared revised outputs to separate code changes from original execution evidence.
- Replaced obsolete Python 3.1 metadata and invalid dependency entries with a Python 3.10+ project configuration and direct requirements. Installation/full run remain unverified without the input data.
- Added focused tests for critical calculation and survey-code boundaries and notebook syntax.
