"""Repeatable retrospective comparison; raw participant data are never written.

November 2026 AI-assisted maintenance, separate from the original group notebook.
The old holdout has already been inspected. Reusing it cannot restore independence.
"""
from pathlib import Path
import hashlib
import io
import importlib.metadata
import math
import platform

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, confusion_matrix, roc_auc_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from imblearn.over_sampling import SMOTENC
from imblearn.pipeline import Pipeline as ImbPipeline

from diabetes_analysis import activity_code, diabetes_label, metrics_from_confusion

NUMERIC = ["RIDAGEYR", "BMXBMI", "LBXGLU", "LBXGLT"]
CATEGORICAL = ["RIAGENDR", "PAQ605"]
FEATURES = NUMERIC + CATEGORICAL
REQUIRED = ["SEQN", "age_group", *FEATURES, "DIQ010", "LBXIN"]


def prepare_data(frame):
    """Validate schema, retain observed target labels, and recode refused activity."""
    missing = set(REQUIRED) - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    frame = frame.copy()
    for name in ["SEQN", *FEATURES, "DIQ010", "LBXIN"]:
        frame[name] = pd.to_numeric(frame[name], errors="raise")
        if np.isinf(frame[name].dropna().to_numpy()).any():
            raise ValueError(f"Infinite value in {name}")
    if frame["SEQN"].isna().any() or frame["SEQN"].duplicated().any():
        raise ValueError("SEQN must be present and unique: duplicates need investigation.")
    for name, allowed in [("DIQ010", {1, 2, 3, 7, 9}), ("RIAGENDR", {1, 2}),
                          ("PAQ605", {1, 2, 7, 9})]:
        unexpected = set(frame[name].dropna()) - allowed
        if unexpected:
            raise ValueError(f"Unexpected {name} codes: {sorted(unexpected)}")
    if (frame[NUMERIC] < 0).any().any():
        raise ValueError("Negative age/BMI/glucose measurements need investigation.")
    labels = frame["DIQ010"].map(diabetes_label)
    valid = labels.notna()
    X = frame.loc[valid, FEATURES].copy()
    X["PAQ605"] = X["PAQ605"].map(activity_code)
    if X.isna().all().any():
        raise ValueError("An entirely missing predictor cannot be imputed defensibly.")
    y = labels.loc[valid].astype(int)
    if y.nunique() != 2 or y.value_counts().min() < 12:
        raise ValueError("Need both target classes and enough minority examples for five folds.")
    return X, y, {"input_rows": len(frame), "labeled_rows": len(X),
        "excluded_target_rows": int((~valid).sum()),
        "target_counts": {str(k): int(v) for k, v in y.value_counts().sort_index().items()},
        "recorded_diq010_counts": {str(k): int(v) for k, v in frame.DIQ010.value_counts(dropna=False).sort_index().items()},
        "missing_by_input_column": {k: int(v) for k, v in frame.isna().sum().items()},
        "duplicate_identifiers": 0,
        "activity_missing_after_recode": int(X["PAQ605"].isna().sum()),
        "age_range_years": [float(frame.RIDAGEYR.min()), float(frame.RIDAGEYR.max())]}


def make_pipeline(model, resample=False):
    """Fit transformations and any resampling only inside each training fold."""
    prepare = ColumnTransformer([
        ("numeric", Pipeline([("impute", SimpleImputer(strategy="median")),
                              ("scale", StandardScaler())]), NUMERIC),
        ("categorical", SimpleImputer(strategy="most_frequent"), CATEGORICAL),
    ], sparse_threshold=0)
    # SMOTENC receives genuine category values after mode imputation, not
    # one-hot columns or standardized codes that ordinary SMOTE interpolates.
    encode = ColumnTransformer([
        ("numeric", "passthrough", list(range(4))),
        ("categorical", OneHotEncoder(handle_unknown="ignore", drop="if_binary",
                                      sparse_output=False), [4, 5]),
    ], sparse_threshold=0)
    steps = [("prepare", prepare)]
    if resample:
        steps.append(("resample", SMOTENC(categorical_features=[4, 5], random_state=42)))
    steps.extend([("encode", encode), ("classifier", model)])
    return ImbPipeline(steps) if resample else Pipeline(steps)


def candidate_specs():
    return [
        ("logistic", make_pipeline(LogisticRegression(solver="liblinear", max_iter=2000,
                                                       random_state=42)),
         {"classifier__C": [0.1, 1.0, 10.0], "classifier__class_weight": [None, "balanced"]}),
        ("forest", make_pipeline(RandomForestClassifier(n_estimators=100, random_state=42,
                                                         n_jobs=1)),
         {"classifier__max_depth": [None, 8], "classifier__class_weight": [None, "balanced"]}),
        ("smotenc_logistic", make_pipeline(LogisticRegression(solver="liblinear",
                       max_iter=2000, random_state=42), resample=True),
         {"classifier__C": [0.1, 1.0, 10.0]}),
    ]


def wilson_interval(successes, trials, z=1.959963984540054):
    """Descriptive binomial interval; ignores selection and NHANES survey design."""
    if trials == 0:
        return None
    p = successes / trials
    center = (p + z*z/(2*trials)) / (1 + z*z/trials)
    radius = z*math.sqrt(p*(1-p)/trials + z*z/(4*trials*trials))/(1 + z*z/trials)
    return [max(0.0, center-radius), min(1.0, center+radius)]


def evaluate(estimator, X, y):
    predicted = estimator.predict(X)
    probability = estimator.predict_proba(X)[:, 1]
    matrix = confusion_matrix(y, predicted, labels=[0, 1]).tolist()
    result = metrics_from_confusion(matrix)
    tn, fp, fn, tp = [n for row in matrix for n in row]
    return {"confusion_matrix": matrix, **result,
            "roc_auc": float(roc_auc_score(y, probability)),
            "average_precision": float(average_precision_score(y, probability)),
            "recall_wilson95_descriptive": wilson_interval(tp, tp+fn),
            "precision_wilson95_descriptive": wilson_interval(tp, tp+fp)}


def run_analysis(path, expected_sha256=None):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Input CSV not found: {path}. See docs/REPRODUCIBILITY.md.")
    raw = path.read_bytes()
    input_sha256 = hashlib.sha256(raw).hexdigest()
    if expected_sha256 is not None and input_sha256 != expected_sha256.lower():
        raise ValueError("Input SHA-256 does not match the expected dataset.")
    X, y, quality = prepare_data(pd.read_csv(io.BytesIO(raw)))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    stratify=y, random_state=1117)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    comparisons, best, best_score = [], None, -float("inf")
    for name, pipeline, grid in candidate_specs():
        search = GridSearchCV(pipeline, grid, scoring="balanced_accuracy", cv=cv,
                              n_jobs=1, error_score="raise", return_train_score=False)
        search.fit(X_train, y_train)
        i = search.best_index_
        comparisons.append({"family": name, "best_parameters": search.best_params_,
            "mean_cv_balanced_accuracy": float(search.best_score_),
            "sd_across_folds": float(search.cv_results_["std_test_score"][i]),
            "candidates": len(search.cv_results_["params"])})
        if search.best_score_ > best_score:
            best_score, best, selected = search.best_score_, search.best_estimator_, name
    # No holdout value has been calculated or used to choose the winner above.
    dummy = DummyClassifier(strategy="constant", constant=0).fit(X_train, y_train)
    result = {"analysis_version": "2026-11-10-retrospective-v1", "input_filename": path.name,
        "input_sha256": input_sha256, "quality": quality,
        "features": FEATURES, "train_rows": len(X_train), "holdout_rows": len(X_test),
        "train_class_counts": {str(k):int(v) for k,v in y_train.value_counts().sort_index().items()},
        "holdout_class_counts": {str(k):int(v) for k,v in y_test.value_counts().sort_index().items()},
        "split_seed":1117,"cv_seed":42,"folds":5,"primary_metric":"balanced_accuracy",
        "threshold":0.5,"comparisons_training_only":comparisons,"selected_family":selected,
        "holdout_selected":evaluate(best,X_test,y_test),"holdout_always_negative":evaluate(dummy,X_test,y_test),
        "limitations":["Retrospective reuse of previously inspected holdout, not an untouched confirmation.",
            "CV winner scores are selection scores, not an unbiased performance estimate.",
            "Small positive sample; descriptive Wilson intervals ignore selection and survey design.",
            "No survey weights/PSU/strata; prepared-subset selection not reconstructed.",
            "Target combines yes and borderline; not future onset, clinical diagnosis or population inference."],
        "environment":{"python":platform.python_version(),**{p:importlib.metadata.version(p)
            for p in ["numpy","pandas","scikit-learn","imbalanced-learn","scipy"]}}}
    return result
