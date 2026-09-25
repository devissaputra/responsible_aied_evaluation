import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import run_uci_study as study


class UCIStudyAdapterTests(unittest.TestCase):
    def test_normalize_target_preserves_endpoint_definition(self):
        raw = pd.Series(["Dropout", "Enrolled", "Graduate", "Dropout"])
        result = study.normalize_target(raw)
        self.assertEqual(result.tolist(), [1, 0, 0, 1])

    def test_normalize_target_rejects_unknown_label(self):
        with self.assertRaisesRegex(ValueError, "unexpected target labels"):
            study.normalize_target(pd.Series(["Dropout", "Mystery"]))

    def test_enrollment_frame_removes_post_enrollment_and_audit_only_fields(self):
        frame = pd.DataFrame(
            {
                "Admission grade": [100, 120],
                "Gender": [0, 1],
                "Nacionality": [1, 2],
                "International": [0, 1],
                "Educational special needs": [0, 1],
                "Curricular units 1st sem (grade)": [12.0, 14.0],
                "Curricular units 2nd sem (approved)": [5, 6],
                "Debtor": [0, 1],
            }
        )
        model, forbidden, audit_only = study.enrollment_feature_frame(frame)
        self.assertEqual(set(audit_only), set(study.AUDIT_ONLY_FIELDS))
        self.assertEqual(len(forbidden), 2)
        self.assertNotIn("Gender", model.columns)
        self.assertNotIn("International", model.columns)
        self.assertNotIn("Educational special needs", model.columns)
        self.assertNotIn("Curricular units 1st sem (grade)", model.columns)
        self.assertIn("Debtor", model.columns)

    def test_audit_labels_use_documented_binary_semantics(self):
        frame = pd.DataFrame(
            {
                "Gender": [0, 1],
                "Nacionality": [1, 41],
                "International": [0, 1],
                "Educational special needs": [0, 1],
            }
        )
        audit = study.build_audit_frame(frame)
        self.assertEqual(audit["gender"].tolist(), ["female", "male"])
        self.assertEqual(audit["international"].tolist(), ["domestic", "international"])
        self.assertEqual(
            audit["nationality_group"].tolist(),
            ["portuguese", "non_portuguese"],
        )
        self.assertEqual(
            audit["special_needs"].tolist(),
            ["no_special_needs_flag", "special_needs_flag"],
        )
        self.assertEqual(
            audit["gender_x_international"].tolist(),
            ["female__domestic", "male__international"],
        )

    def test_audit_labels_reject_unknown_gender_code(self):
        frame = pd.DataFrame(
            {
                "Gender": [2],
                "Nacionality": [1],
                "International": [0],
                "Educational special needs": [0],
            }
        )
        with self.assertRaisesRegex(ValueError, "unexpected Gender codes"):
            study.build_audit_frame(frame)

    def test_dataset_fingerprint_is_deterministic_and_sensitive(self):
        X = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
        y = pd.Series(["Dropout", "Graduate"])
        first = study.dataset_fingerprint(X, y)
        second = study.dataset_fingerprint(X.copy(), y.copy())
        self.assertEqual(first, second)
        changed = X.copy()
        changed.loc[0, "a"] = 99
        self.assertNotEqual(first, study.dataset_fingerprint(changed, y))

    def test_calibration_slope_intercept_is_finite(self):
        probability = np.array([0.05, 0.2, 0.4, 0.6, 0.8, 0.95])
        outcome = np.array([0, 0, 0, 1, 1, 1])
        result = study.calibration_slope_intercept(probability, outcome)
        self.assertTrue(np.isfinite(result["intercept"]))
        self.assertTrue(np.isfinite(result["slope"]))

    def test_group_audit_does_not_score_underpowered_comparison(self):
        indices = np.arange(20)
        probability = np.linspace(0.1, 0.9, 20)
        outcome = np.array([0, 1] * 10)
        labels = pd.Series(["a"] * 10 + ["b"] * 10)
        result = study.group_audit(indices, probability, outcome, labels)
        self.assertEqual(result["fairness_metrics"]["status"], "not_evaluable")
        self.assertIsNone(result["fairness_metrics"]["selection_rate_gap"])

    def test_governance_context_produces_no_deployment_verdict(self):
        result = study.governance_and_risk_context()
        self.assertFalse(result["deployment_review_executed"])
        self.assertFalse(result["governance_evidence_gap"]["complete"])
        self.assertIn("not a deployment review", result["interpretation"].lower())


if __name__ == "__main__":
    unittest.main()
