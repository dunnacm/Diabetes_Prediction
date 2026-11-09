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

The revised notebook retains that broad structure and the original numeric coding of binary fields to keep changes bounded. It corrects identified implementation and reporting issues but has not been run on the missing dataset. It is not a validated recreation of the historical results.

## Reading the figures

Original PNGs in `notebooks/` and the archived executed notebook are retained unchanged. They include historical class-label shorthand, preprocessing choices and metrics. Use the definitions and limitations in this documentation when interpreting them. The revised notebook writes new figures to ignored `reports/generated/` instead of silently replacing original figures.
