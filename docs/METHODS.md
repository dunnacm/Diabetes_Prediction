# Methods and data dictionary

## Data and target

The notebook identifies its input as a prepared NHANES 2013-2014 subset named `NHANES_age_prediction.csv`. That CSV is absent from the repository. Its saved output reports 2,278 rows and ten columns. The precise extraction and sample-selection process is not documented here, so the full original survey must not be equated with this subset.

| Original field | Notebook name | Use |
| --- | --- | --- |
| SEQN | ID | Identifier; excluded from predictors |
| RIDAGEYR | Age | Predictor |
| RIAGENDR | Gender | Coded survey field; predictor, not inferred gender identity |
| PAQ605 | Physical_Activity | Vigorous **work** activity; predictor |
| BMXBMI | BMI | Predictor |
| LBXGLU | Glucose_Level | Predictor |
| DIQ010 | Diabetes_Status | Source of target; excluded from predictors |
| LBXGLT | Oral_Glucose_Test | Predictor |
| LBXIN | Insulin_Level | Excluded |
| age_group | age_group | Excluded |

The project maps DIQ010 values 1 and 3 to positive and 2 to negative; other responses are excluded from the labeled set. Borderline is grouped with yes by project choice. CDC describes DIQ010 as a report of having been told by a doctor that the participant has diabetes. [CDC diabetes codebook](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/DIQ_H.htm#DIQ010).

The original notebook changed PAQ605 code 7 to 2, calling it an accidental value. CDC identifies 7 as refused and 9 as do not know; 1 and 2 mean yes and no. The revised notebook treats 7 and 9 as missing, to be handled in training preprocessing. This changes the analysis and requires new evaluation. PAQ605 measures vigorous work activity, not all exercise. [CDC physical-activity codebook](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/PAQ_H.htm#PAQ605).

## Original workflow

- Stratified 80/20 split, random seed 1117.
- Median imputation and standard scaling for numeric fields; categorical pipeline available but original selected fields were numeric codes.
- Five-fold shuffled stratified cross-validation, seed 42, on the training set.
- Logistic regression and random-forest baselines.
- GridSearchCV over 28 combinations, using training-fold balanced accuracy; saved best setting is logistic regression, C=10, L2 penalty, balanced class weighting.
- Separate SMOTE, random undersampling and logistic-regression pipeline; sampling remains inside the training pipeline.
- Holdout confusion matrices and multiple metrics; exploratory coefficients, permutation importance and SHAP sections.

The revised exploratory notebook retains that broad structure and the original numeric coding of binary fields. It has not been executed end to end. The current reproducible comparison is the separate CLI described below; historical and newly executed results remain separate.

## Current reproducible comparison (November 10, 2026)

- Participant is the data grain; duplicate SEQN values stop the run. No joins or weights are introduced. See [input inventory and provenance](DATA_PROVENANCE.md).
- Age (years), BMI and the two glucose measurements are quantitative predictors. The prepared-file units for BMI and glucose are not independently documented by the recovery; they are used as supplied and must be reconciled to their exact laboratory codebooks before clinical interpretation.
- RIAGENDR and PAQ605 are explicitly categorical, regardless of their integer storage type. RIAGENDR is a binary survey sex code, not an inferred identity. Numeric median imputation/scaling and categorical mode imputation are fitted inside each training fold.
- Optional [SMOTENC](https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTENC.html) receives numeric measurements and identified categorical columns, then one-hot encoding precedes the classifier. This avoids ordinary SMOTE creating fractional survey categories. The standard SMOTE plus redundant full balancing/undersampling experiment remains historical.
- The 80/20 stratified seed 1117 split is reused only for retrospective comparability. Five-fold stratified CV, seed 42, compares six logistic settings, four random-forest settings and three SMOTENC-logistic settings. Selection uses mean training-CV balanced accuracy only, before holdout metrics are computed. The fold standard deviation is variability across folds, not a confidence interval.
- The selected model and an always-negative reference are then reported at the fixed default classification threshold 0.5. No threshold tuning or holdout-guided model choice is performed in the CLI.
- Confusion matrices, both F1 definitions, positive precision/recall, balanced accuracy, G-mean, ROC-AUC and average precision are recorded. Descriptive Wilson intervals for positive recall/precision show small denominators; they ignore survey design, model selection and prior holdout reuse.

The CLI does not generate permutation or SHAP interpretations. Those notebook sections remain exploratory and unverified through clean execution. It also does not estimate causal effects, calibrated disease probabilities or future onset.

## Reading the figures

Original PNGs in `notebooks/` and the archived executed notebook are retained unchanged. They include historical class-label shorthand, preprocessing choices and metrics. Use the definitions and limitations in this documentation when interpreting them. The revised notebook writes new figures to ignored `reports/generated/` instead of silently replacing original figures.

Two historical plots were inspected visually in the November 10 review. The tuned confusion matrix overlays outcome-specific colors on a percentage heatmap while retaining the heatmap colorbar; those colors do not truthfully encode the colorbar scale. Read the cell values and documented denominators, not the colorbar. The combined boxplot puts age, BMI and glucose on a shared axis despite different units, compressing the smaller-scale variables, and its class legend omits borderline. For a new explanatory figure, use a single sequential 0–100% confusion-matrix scale and separate distribution panels with explicit units and yes/borderline labels. Historical image bytes are preserved rather than silently redrawn.
