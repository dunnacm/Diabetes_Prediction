# Input provenance and data quality

The November 10, 2026 run used a locally recovered `NHANES_age_prediction.csv`. The repository does not redistribute participant-level records. Supply an authorized copy using the command in [REPRODUCIBILITY](REPRODUCIBILITY.md).

| Property | Verified observation |
| --- | --- |
| SHA-256 of recovered input | `a5e588ef5d015349b2656b2905cd2ac9603381643e188a5587a58cf5f972354d` |
| Grain | One row per unique SEQN participant identifier |
| Shape | 2,278 rows, 10 columns |
| Target source | DIQ010: 2,199 no; 21 yes; 58 borderline |
| Modeling target | 79 positives (yes OR borderline), 2,199 negatives |
| Age range | 12 through 80 years; this is not an adult-only sample |
| Activity exception | One PAQ605 refused response (7), converted to missing, then imputed within training folds |
| Missing values / duplicate identifiers | No raw missing cells or duplicate identifiers; missingness is introduced by the documented activity recode |

The filename, shape, first five records and class counts agree with the original saved notebook. There is no original input checksum. These matches support this as the recovered candidate input; they do not prove byte identity with the 2025 input, authorship or historical clean execution. Private recovery paths and academic materials are not included in this public repository.

## Definitions and authority

The notebook identifies the data as a prepared NHANES 2013–2014 subset. The CDC codebooks govern the meanings of the survey fields; they do not establish how this prepared subset was selected. [DIQ010](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/DIQ_H.htm#DIQ010) is reported diagnosis, with borderline a distinct response. [PAQ605](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/PAQ_H.htm#PAQ605) is vigorous work activity, including unpaid work, rather than general exercise. Both pages were checked November 10, 2026.

Unknown sample-selection criteria, survey weights, strata and primary sampling units remain unresolved. Laboratory eligibility and measurement timing also matter. The prepared file cannot support population-weighted NHANES inference, incidence prediction or clinical performance claims. Most positive labels here are borderline (58 of 79), which should stay visible in any description of the task.

## Relationships and handling

No join is performed. SEQN is used for uniqueness validation and excluded from predictors. DIQ010 supplies the target and is excluded from predictors. `age_group` and LBXIN are retained only as source-schema checks; they are not predictors. The runner rejects unknown category codes, duplicate identifiers, nonnumeric measurements and infinite or negative quantitative predictor values rather than silently repairing them. Missing target responses are excluded; predictor imputation is fitted within each training fold. Aggregate counts and the exact input checksum are saved in the run report.

The public report contains aggregate results only. No raw rows, participant identifiers, model objects, private academic documents or original papers are published by this revision.
