# Findings and interpretation

## The important result is a tradeoff

In the original saved test results, both baseline models correctly label 439 of 440 negative cases but detect none of the 16 positive cases. Their 96.27% accuracy therefore hides failure on the minority class. An always-negative classifier would score 440/456, or 96.49%, accuracy on this same test set.

The tuned logistic regression detects 10 of 16 positives and misses six. It also produces 95 false positives, so only 10 of its 105 positive predictions are true positives. The resampling pipeline detects the same ten positives but produces 103 false positives. The saved comparison supports discussing the precision-recall tradeoff; it does not establish a usable screening system or the superiority of a method in new populations.

## What each metric answers

- Accuracy: how many predictions are correct overall?
- Positive recall: how many actual positive labels were detected?
- Positive precision: how many positive predictions were correct?
- Balanced accuracy: the average of positive recall and negative recall.
- Positive F1: the harmonic mean of positive precision and recall.
- Macro F1: the average F1 across both classes. This is what the original notebook calculated, despite printing a positive-class F1 label.
- G-mean: the geometric mean of the two class recalls.
- ROC-AUC: ranking quality across thresholds; it cannot be reconstructed from one confusion matrix.

`scripts/summarize_saved_results.py` recomputes the confusion-matrix metrics using only Python's standard library. It does not train a model or validate the source observations. Original ROC-AUC values are kept separately as notebook-reported values in the JSON evidence.

## Interpretation of predictors

The notebook contains coefficients, permutation importance and SHAP figures. These can describe how a fitted model uses its inputs, but they do not show that a feature causes diabetes. The original permutation importance uses default accuracy, whereas tuning uses balanced accuracy; rankings across those criteria should not be treated as interchangeable. The revised notebook specifies balanced accuracy for permutation importance.

Glucose measurements are contemporaneous with the survey-derived label. Their usefulness here does not show that the model forecasts disease before clinical information is available. The original SHAP waterfall cell also referenced a different variable from the explainer defined in the notebook; saved figures are historical artifacts, not proof of a successful clean execution.

## Limits and next research steps

### New executed evidence

The November 10 CLI run selected balanced logistic regression with C=10 by training-only CV. On the reused holdout, it again detects 10 of 16 positives, with 95 false positives. ROC-AUC is 0.77372 and average precision is 0.10865; the holdout positive fraction is 16/456 (0.03509). Average precision is based on ranked scores and is not trapezoidal PR-AUC. These are new run results, separate from the saved historical outputs.

Descriptive 95% Wilson intervals are 38.6%–81.5% for recall and 5.3%–16.6% for precision. They illustrate denominator sensitivity, not unbiased population uncertainty: survey design, model-selection variability and prior test reuse are not accounted for. Most positives are borderline responses, so “detecting diabetes” without that qualification overstates the modeled task.

### Remaining work

1. Reconstruct the prepared subset's selection and extraction. The recovered candidate's checksum, first-record agreement and schema are documented; exact identity with the original remains unproven.
2. The new CLI completed in an isolated environment. A clean execution of the earlier exploratory notebook and optional SHAP remains unverified.
3. Examine the decision to combine borderline and yes responses; do not present it as an official clinical threshold.
4. Choose model, thresholds and metrics within training/validation data before consulting a genuinely untouched test set. The original discussion mentions test-set model selection, which limits claims of unbiased final evaluation.
5. Report uncertainty, calibrate probabilities if probability use is intended, and consider precision-recall curves for the rare positive class.
6. The new CLI compares categorical-aware SMOTENC inside training validation. Its CV result did not displace the weighted logistic model. That does not establish general superiority; the old ordinary-SMOTE experiment remains historical.
7. Address NHANES survey design, weights and subset selection before population-level inference. External validation would be a separate study.

No medical recommendations are made by this project.
