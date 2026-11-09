"""Small auditable helpers. No model fitting or third-party dependencies."""
import math

def diabetes_label(value):
    """Project choice: yes or borderline -> 1; no -> 0; other/missing -> NaN."""
    return {1: 1.0, 2: 0.0, 3: 1.0}.get(value, float("nan"))

def activity_code(value):
    """PAQ605: retain yes/no; refused, unknown and missing are not 'no'."""
    return float(value) if value in (1, 2) else float("nan")

def metrics_from_confusion(matrix):
    """Rows are actual 0/1; columns predicted 0/1. Undefined ratios use zero."""
    if len(matrix) != 2 or any(len(row) != 2 for row in matrix):
        raise ValueError("Expected a 2 by 2 confusion matrix")
    values = [x for row in matrix for x in row]
    if any(isinstance(x, bool) or not isinstance(x, int) or x < 0 for x in values):
        raise ValueError("Counts must be nonnegative integers")
    tn, fp, fn, tp = values
    if tn + fp == 0 or tp + fn == 0:
        raise ValueError("Both actual classes must have observations")
    div = lambda a, b: a / b if b else 0.0
    sensitivity = div(tp, tp + fn)
    specificity = div(tn, tn + fp)
    positive_f1 = div(2 * tp, 2 * tp + fp + fn)
    negative_f1 = div(2 * tn, 2 * tn + fp + fn)
    return {"accuracy": div(tp + tn, sum(values)),
            "balanced_accuracy": (sensitivity + specificity) / 2,
            "positive_recall": sensitivity, "positive_precision": div(tp, tp + fp),
            "positive_f1": positive_f1, "macro_f1": (positive_f1 + negative_f1) / 2,
            "g_mean": math.sqrt(sensitivity * specificity)}
