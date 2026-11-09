# Diabetes status classification with NHANES survey data

An academic group project from **Data Mining and Text Analytics (MATH 3310), Fall 2025**, comparing logistic regression and random forests on a strongly imbalanced survey-derived label.

**The main lesson:** a model can have high accuracy while missing every positive case. The saved baseline results do exactly that. Class weighting improves positive-case detection, but produces many more false positives. Understanding that tradeoff matters more than reporting accuracy alone.

## Start here

- **Understand the results:** [Findings and interpretation](docs/FINDINGS.md).
- **Understand the analysis:** [Methods and data dictionary](docs/METHODS.md).
- **Run or inspect the work:** [Reproduction guide](docs/REPRODUCIBILITY.md).
- **See the original evidence:** [Original executed notebook](notebooks/archive/Final_original.ipynb).
- **Inspect the revised code:** [Revised notebook](notebooks/Final.ipynb).
- **Credit and revision history:** [Attribution](docs/ATTRIBUTION.md) and [changes](CHANGELOG.md).

## Purpose

Can demographic, activity and laboratory measurements help distinguish participants who reported diabetes or borderline diabetes from those who reported no diabetes in the supplied NHANES subset?

The target combines `DIQ010=1` (yes) and `DIQ010=3` (borderline) into class 1; `DIQ010=2` is class 0. This is a modeling decision, not a clinical diagnosis. The analysis classifies a reported status; it does **not** forecast future diabetes onset.

## What the saved results show

The original notebook records 2,278 observations: 2,199 negatives and 79 positives. Its held-out set has 440 negatives and just 16 positives.

| Original model | Accuracy | Balanced accuracy | Positive recall | Positive precision | False positives |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline logistic regression | 96.27% | 49.89% | 0.00% | 0.00% | 1 |
| Baseline random forest | 96.27% | 49.89% | 0.00% | 0.00% | 1 |
| Tuned, class-weighted logistic regression | 77.85% | 70.45% | 62.50% | 9.52% | 95 |
| SMOTE + undersampling + logistic regression | 76.10% | 69.55% | 62.50% | 8.85% | 103 |

**Evidence status:** these figures are recalculated from confusion matrices saved in the original notebook, not from a new model run. The revised notebook has cleared outputs and changes to data handling; these historical figures must not be attributed to the revised code. [Exact values and provenance](reports/results/original_saved_results.json).

## Approach and tools

1. Define the outcome, check values and explore the class imbalance.
2. Use an 80/20 stratified split and preprocessing pipelines to keep fitted transformations inside training.
3. Compare logistic regression and random forests using five-fold stratified cross-validation; tune with balanced accuracy.
4. Compare class weighting with a resampling pipeline.
5. Examine confusion matrices, precision/recall, macro and positive-class F1, G-mean and ROC-AUC, followed by coefficients, permutation importance and optional SHAP explanations.

**Tools:** Python, pandas, NumPy, scikit-learn, imbalanced-learn, Matplotlib, Seaborn and Jupyter; SHAP for optional interpretation. The original notebook also used problexity for exploratory complexity measures.

## Current status and limits

The input `NHANES_age_prediction.csv` is **not included**. You can read the report and verify the arithmetic without it; training requires the exact prepared input. No external validation, clinical use, production deployment or population-weighted NHANES inference is established. Only 16 positive cases appear in the saved test set, so small changes in predictions have large effects on recall.

This fork preserves the [original group repository](https://github.com/bpickett14/Diabetes_Prediction) and its commit history. The November 2026 review improves documentation, corrects identified code issues and adds auditable result checks. It does not claim sole authorship of the coursework or a newly validated model.
