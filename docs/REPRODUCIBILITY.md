# Reproduction guide

## What works without the dataset

From the repository root, using Python 3.10 or newer:

```bash
python scripts/summarize_saved_results.py
python -m unittest discover -s tests -v
```

These use only the standard library. Tests verify confusion-matrix calculations, distinguish macro F1 from positive F1, check survey-code handling, and compile every revised notebook code cell. They do not fit or validate a model.

## Run the analysis when the original input is available

Use Python 3.12 in a new environment. Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m jupyterlab
```

macOS/Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyterlab
```

Place the authorized, exact prepared CSV at `data/raw/NHANES_age_prediction.csv`, then open `notebooks/Final.ipynb`, restart the kernel and run all cells in order. The loader stops with a clear message if the data are missing and checks required columns. Raw data remain ignored by Git.

The notebook's core model comparison does not require SHAP. To use the optional interpretation section, also install `requirements-interpretation.txt`. Complexity analysis was retained in the archived original only; it is not a necessary preprocessing or evaluation step.

## Validation status

The November 2026 revision passed local standard-library tests and Python syntax checks. A fresh installation of the modeling dependencies and a complete notebook run have **not** been verified. Requirements name the actual imported packages and fix the original invalid `matplotlib.pyplot` package entry; they are not a locked, reproduced environment.

The historical JSON and original executed notebook remain separate from the revised notebook, whose outputs were cleared. New predictions will differ after corrected survey-code handling. Do not relabel the historical table as a result of revised code.

Before making a new performance claim, record the input checksum, package versions, split and CV seeds, preprocessing choices and full outputs. Keep evaluation thresholds and model selection independent of the final test set. Do not upload participant-level data simply to make the notebook run.
