"""Recompute historical arithmetic without importing or fitting a model."""
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from diabetes_analysis import metrics_from_confusion

def main():
    evidence = json.loads((ROOT / "reports/results/original_saved_results.json").read_text(encoding="utf-8"))
    print(evidence["status"])
    for model in evidence["models"]:
        metrics = metrics_from_confusion(model["confusion_matrix"])
        print(model["name"])
        print(json.dumps(metrics, sort_keys=True))

if __name__ == "__main__":
    main()
