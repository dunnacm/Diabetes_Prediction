# Changes

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
