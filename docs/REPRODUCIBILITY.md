# Reproduction guide

## Check historical arithmetic without data or third-party packages

From the repository root:

```bash
python scripts/summarize_saved_results.py
python -m unittest discover -s tests -p test_review.py -v
```

These seven checks recalculate historical confusion-matrix metrics, check survey-code handling and compile revised notebook cells. They do not fit a model.

## Run the current comparison

The recommended reproducible entry point is `scripts/reproduce_analysis.py`. It replaces the exploratory notebook as the current model-comparison path. Python 3.12.14 on Windows was tested in a fresh isolated environment. The pinned reproduction requirements record the versions actually installed.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-reproduction.txt
python -m unittest discover -s tests -v
python scripts/reproduce_analysis.py --data "PATH/TO/NHANES_age_prediction.csv" --expected-sha256 a5e588ef5d015349b2656b2905cd2ac9603381643e188a5587a58cf5f972354d
```

On macOS/Linux, create the environment with `python3.12 -m venv .venv` and activate with `source .venv/bin/activate`; the subsequent Python commands are the same. Those platforms were not tested. Supply an authorized local input; see [provenance](DATA_PROVENANCE.md). The optional checksum argument verifies the recovered input used for the recorded run. Leave it out only when intentionally analyzing a different prepared input and documenting the change.

By default, aggregate output goes to ignored `reports/generated/reproduction.json`. Use `--output PATH` to choose another destination. The script works when invoked by its absolute path from another working directory. It exports no participant rows or identifiers. Input and output paths may contain spaces.

## What was actually checked

- A fresh isolated environment was installed, then the current CLI completed on the recovered 2,278-row input.
- The full test suite checks historical metrics and notebook syntax, unknown survey codes, missing-target exclusions, duplicate identifiers, training-only imputation, valid SMOTENC categories and descriptive interval arithmetic.
- [The recorded run](../reports/results/reproduction_2026-11-10.json) contains the input checksum, schema-quality counts, split and CV seeds, training-only selection results, aggregate holdout results and package versions.
- The original executed notebook and all original PNGs were hash-checked and preserved.

This is **retrospective reproducibility, not independent validation**. The same previously examined holdout is reused. No claim that the test set is newly untouched is made. The selected model and an always-negative reference are evaluated after training-only model selection; holdout results are not used to choose a candidate in this runner.

## Notebook and interpretation boundary

`notebooks/archive/Final_original.ipynb` is immutable historical evidence. `notebooks/Final.ipynb` is a revised exploratory notebook from the earlier review, with outputs cleared and an explicit current-status notice. It still includes the original ordinary-SMOTE comparison and repeated exploratory holdout use. Its code has been syntax checked, but neither a complete clean notebook execution nor the optional SHAP path has been verified. Its outputs must not be substituted for the recorded CLI results.

`requirements.txt` and `requirements-interpretation.txt` remain optional notebook dependencies; they are not the environment lock for the current runner. Permutation/SHAP outputs are not recomputed by the CLI. Their historical plots remain artifacts requiring the documented cautions, not new validated explanations. No model is approved for clinical use or deployment.
