import ast
import json
import math
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from diabetes_analysis import activity_code, diabetes_label, metrics_from_confusion

class ReviewTests(unittest.TestCase):
    def test_refused_is_not_no(self):
        self.assertEqual(activity_code(2), 2)
        for code in (7, 9, None, float("nan")):
            self.assertTrue(math.isnan(activity_code(code)))

    def test_target_borderline_is_explicit(self):
        self.assertEqual(diabetes_label(3), 1)
        self.assertEqual(diabetes_label(2), 0)
        self.assertTrue(math.isnan(diabetes_label(7)))

    def test_macro_f1_is_not_positive_f1(self):
        m = metrics_from_confusion([[439, 1], [16, 0]])
        self.assertEqual(m["positive_f1"], 0)
        self.assertAlmostEqual(m["macro_f1"], 0.49050279329608937)
        self.assertAlmostEqual(m["accuracy"], 439 / 456)

    def test_tuned_tradeoff(self):
        m = metrics_from_confusion([[345, 95], [6, 10]])
        self.assertAlmostEqual(m["positive_recall"], 10 / 16)
        self.assertAlmostEqual(m["positive_precision"], 10 / 105)
        self.assertAlmostEqual(m["positive_f1"], 20 / 121)

    def test_invalid_counts_rejected(self):
        for matrix in ([[1, -1], [2, 3]], [[1, 2]], [[1, 2], [0, 0]]):
            with self.assertRaises(ValueError): metrics_from_confusion(matrix)

    def test_saved_matrices_have_consistent_support(self):
        j = json.loads((ROOT / "reports/results/original_saved_results.json").read_text(encoding="utf-8"))
        for m in j["models"]:
            self.assertEqual([sum(row) for row in m["confusion_matrix"]], [440, 16])

    def test_notebook_code_compiles_and_has_no_stale_outputs(self):
        j = json.loads((ROOT / "notebooks/Final.ipynb").read_text(encoding="utf-8"))
        for i, c in enumerate(j["cells"]):
            if c["cell_type"] == "code":
                ast.parse("".join(c["source"]), filename=f"cell {i}")
                self.assertEqual(c["outputs"], [])
                self.assertIsNone(c["execution_count"])

if __name__ == "__main__": unittest.main()
