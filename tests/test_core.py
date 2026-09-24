import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from responsible_aied_evaluation import core


def records():
    return [
        core.EvaluationRecord("A1", 0.90, 1, "A", "A_mobile"),
        core.EvaluationRecord("A2", 0.80, 1, "A", "A_desktop"),
        core.EvaluationRecord("A3", 0.70, 0, "A", "A_mobile"),
        core.EvaluationRecord("A4", 0.40, 0, "A", "A_desktop"),
        core.EvaluationRecord("B1", 0.85, 1, "B", "B_mobile"),
        core.EvaluationRecord("B2", 0.55, 1, "B", "B_desktop"),
        core.EvaluationRecord("B3", 0.45, 0, "B", "B_mobile"),
        core.EvaluationRecord("B4", 0.20, 0, "B", "B_desktop"),
    ]


def governance(**overrides):
    base = {
        "privacy_reviewed": True,
        "accessibility_reviewed": True,
        "human_oversight_defined": True,
        "appeal_path_defined": True,
        "rollback_plan_defined": True,
        "monitoring_plan_defined": True,
        "decision_owner": "Responsible AI Review Board",
        "privacy_evidence": "Privacy impact assessment PIA-01",
        "accessibility_evidence": "Accessibility review A11Y-01",
        "human_oversight_owner": "Academic operations lead",
        "appeal_path": "Learner appeal and instructor escalation procedure",
        "rollback_owner": "Product safety owner",
        "monitoring_plan": "Monthly drift and incident review",
    }
    base.update(overrides)
    return core.GovernanceReview(**base)


def config(**overrides):
    base = {
        "probability_threshold": 0.5,
        "max_ece": 0.30,
        "max_brier": 0.25,
        "max_selection_rate_gap": 0.40,
        "max_tpr_gap": 0.40,
        "max_fpr_gap": 0.60,
        "min_group_size": 4,
        "max_open_risk_score": 12,
    }
    base.update(overrides)
    return core.DecisionConfig(**base)


class CoreTests(unittest.TestCase):
    def test_record_validation(self):
        with self.assertRaises(ValueError):
            core.EvaluationRecord("x", 1.2, 1, "A")

    def test_record_rejects_nan(self):
        with self.assertRaises(ValueError):
            core.EvaluationRecord("x", math.nan, 1, "A")

    def test_duplicate_case_ids_rejected(self):
        rows = records()
        rows.append(
            core.EvaluationRecord("A1", 0.2, 0, "B")
        )
        with self.assertRaises(ValueError):
            core.predictions_at_threshold(rows)

    def test_threshold_predictions(self):
        result = core.predictions_at_threshold(
            records(),
            0.5,
        )
        self.assertEqual(
            result,
            [1, 1, 1, 0, 1, 1, 0, 0],
        )

    def test_confusion_metrics(self):
        result = core.confusion_metrics(
            [1, 1, 0, 0],
            [1, 0, 1, 0],
        )
        self.assertEqual(result["tp"], 1)
        self.assertEqual(result["fp"], 1)
        self.assertEqual(result["fn"], 1)
        self.assertEqual(result["tn"], 1)
        self.assertAlmostEqual(result["accuracy"], 0.5)

    def test_confusion_handles_undefined_precision(self):
        result = core.confusion_metrics(
            [0, 0],
            [0, 1],
        )
        self.assertIsNone(result["precision"])

    def test_calibration_bins_return_counts(self):
        rows = core.calibration_bins(
            [0.1, 0.2, 0.8, 0.9],
            [0, 0, 1, 1],
            bins=2,
        )
        self.assertEqual(
            sum(row["count"] for row in rows),
            4,
        )

    def test_ece_known_example(self):
        self.assertAlmostEqual(
            core.expected_calibration_error(
                [0.9, 0.8, 0.2, 0.1],
                [1, 1, 0, 0],
            ),
            0.15,
        )

    def test_mce(self):
        value = core.maximum_calibration_error(
            [0.9, 0.8, 0.2, 0.1],
            [1, 1, 0, 0],
            bins=2,
        )
        self.assertAlmostEqual(value, 0.15)

    def test_brier_score(self):
        value = core.brier_score(
            [0.9, 0.1],
            [1, 0],
        )
        self.assertAlmostEqual(value, 0.01)

    def test_demographic_parity_requires_two_groups(self):
        with self.assertRaises(ValueError):
            core.demographic_parity_difference(
                [1, 0],
                ["A", "A"],
            )

    def test_demographic_parity_gap(self):
        value = core.demographic_parity_difference(
            [1, 1, 0, 0],
            ["A", "A", "B", "B"],
        )
        self.assertEqual(value, 1.0)

    def test_group_performance_returns_counts(self):
        report = core.group_performance(
            records(),
            min_group_size=4,
        )
        self.assertEqual(
            report["groups"]["A"]["n"],
            4,
        )
        self.assertEqual(report["warnings"], [])

    def test_group_performance_warns_small_group(self):
        report = core.group_performance(
            records(),
            min_group_size=5,
        )
        self.assertEqual(len(report["warnings"]), 2)

    def test_single_group_is_not_evaluable(self):
        subset = records()[:4]
        report = core.fairness_report(
            subset,
            min_group_size=1,
        )
        self.assertEqual(
            report["status"],
            "not_evaluable",
        )
        self.assertIsNone(
            report["selection_rate_gap"]
        )

    def test_fairness_report_contains_error_gaps(self):
        report = core.fairness_report(
            records(),
            min_group_size=4,
        )
        self.assertEqual(report["status"], "scored")
        self.assertIn("tpr_gap", report)
        self.assertIn("fpr_gap", report)
        self.assertIn("equalized_odds_gap", report)

    def test_intersectional_group_analysis(self):
        report = core.fairness_report(
            records(),
            group_field="intersectional_group",
            min_group_size=1,
        )
        self.assertEqual(report["status"], "scored")
        self.assertEqual(len(report["groups"]), 4)

    def test_group_calibration(self):
        report = core.group_calibration_report(
            records(),
            bins=2,
            min_group_size=4,
        )
        self.assertEqual(report["status"], "scored")
        self.assertIn("ece_gap", report)
        self.assertIn("brier_gap", report)

    def test_group_calibration_single_group_not_evaluable(self):
        report = core.group_calibration_report(
            records()[:4],
            min_group_size=1,
        )
        self.assertEqual(
            report["status"],
            "not_evaluable",
        )

    def test_bootstrap_accuracy_interval(self):
        result = core.bootstrap_interval(
            records(),
            "accuracy",
            n_resamples=50,
            seed=1,
        )
        self.assertEqual(result["status"], "scored")
        self.assertLessEqual(
            result["lower"],
            result["point"],
        )
        self.assertGreaterEqual(
            result["upper"],
            result["point"],
        )

    def test_bootstrap_fairness_interval(self):
        result = core.bootstrap_interval(
            records(),
            "selection_rate_gap",
            n_resamples=50,
            seed=2,
        )
        self.assertEqual(result["status"], "scored")

    def test_bootstrap_rejects_bad_metric(self):
        with self.assertRaises(ValueError):
            core.bootstrap_interval(
                records(),
                "mystery",
                n_resamples=10,
            )

    def test_threshold_sensitivity(self):
        rows = core.threshold_sensitivity(
            records(),
            thresholds=(0.4, 0.5, 0.6),
            min_group_size=4,
        )
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[1]["threshold"], 0.5)

    def test_compare_scenarios(self):
        shifted = [
            core.EvaluationRecord(
                record.case_id,
                min(1.0, record.probability + 0.1),
                record.outcome,
                record.group,
                record.intersectional_group,
            )
            for record in records()
        ]
        report = core.compare_scenarios(
            records(),
            shifted,
            min_group_size=4,
        )
        self.assertIn("delta", report)
        self.assertIn("ece", report["delta"])

    def test_governance_requires_boolean(self):
        with self.assertRaises(ValueError):
            core.GovernanceReview(
                privacy_reviewed="yes",
                accessibility_reviewed=True,
                human_oversight_defined=True,
                appeal_path_defined=True,
                rollback_plan_defined=True,
                monitoring_plan_defined=True,
                decision_owner="owner",
            )

    def test_governance_report_complete(self):
        report = core.governance_report(governance())
        self.assertTrue(report["complete"])

    def test_governance_true_without_evidence_fails(self):
        report = core.governance_report(
            governance(privacy_evidence=None)
        )
        self.assertFalse(report["complete"])
        self.assertIn(
            "privacy",
            report["failed_checks"],
        )

    def test_risk_item_score(self):
        risk = core.RiskItem(
            "R1",
            "Missed support",
            4,
            3,
            "Human review",
            owner="Safety lead",
        )
        self.assertEqual(risk.risk_score, 12)

    def test_risk_item_rejects_bad_severity(self):
        with self.assertRaises(ValueError):
            core.RiskItem(
                "R1",
                "risk",
                6,
                1,
                "mitigate",
            )

    def test_risk_summary(self):
        summary = core.risk_register_summary(
            [
                core.RiskItem(
                    "R1",
                    "risk",
                    4,
                    3,
                    "mitigate",
                ),
                core.RiskItem(
                    "R2",
                    "risk2",
                    2,
                    2,
                    "mitigate",
                    status="mitigated",
                ),
            ]
        )
        self.assertEqual(summary["open_count"], 1)
        self.assertEqual(
            summary["highest_open_risk_score"],
            12,
        )

    def test_config_requires_explicit_valid_thresholds(self):
        with self.assertRaises(ValueError):
            core.DecisionConfig(
                probability_threshold=0.5,
                max_ece=1.2,
                max_brier=0.2,
                max_selection_rate_gap=0.1,
                max_tpr_gap=0.1,
                max_fpr_gap=0.1,
                min_group_size=4,
                max_open_risk_score=12,
            )

    def test_decision_passes_complete_low_risk_case(self):
        report = core.responsible_aied_decision(
            records(),
            governance(),
            [
                core.RiskItem(
                    "R1",
                    "Minor usability issue",
                    2,
                    2,
                    "Monitor",
                    owner="UX lead",
                )
            ],
            config(),
        )
        self.assertEqual(report["decision"], "PASS")

    def test_decision_blocks_missing_governance(self):
        report = core.responsible_aied_decision(
            records(),
            governance(rollback_owner=None),
            [],
            config(),
        )
        self.assertEqual(report["decision"], "BLOCK")
        self.assertTrue(
            any(
                "governance" in reason
                for reason in report["blocking_reasons"]
            )
        )

    def test_decision_blocks_high_open_risk(self):
        report = core.responsible_aied_decision(
            records(),
            governance(),
            [
                core.RiskItem(
                    "R1",
                    "Severe missed support",
                    5,
                    4,
                    "Redesign",
                    owner="Safety lead",
                )
            ],
            config(),
        )
        self.assertEqual(report["decision"], "BLOCK")

    def test_decision_conditional_for_small_groups(self):
        report = core.responsible_aied_decision(
            records(),
            governance(),
            [],
            config(min_group_size=5),
        )
        self.assertEqual(
            report["decision"],
            "CONDITIONAL",
        )

    def test_decision_not_evaluable_with_one_group(self):
        report = core.responsible_aied_decision(
            records()[:4],
            governance(),
            [],
            config(min_group_size=1),
        )
        self.assertEqual(
            report["decision"],
            "NOT_EVALUABLE",
        )

    def test_decision_blocks_metric_violation(self):
        report = core.responsible_aied_decision(
            records(),
            governance(),
            [],
            config(max_selection_rate_gap=0.0),
        )
        self.assertEqual(report["decision"], "BLOCK")

    def test_legacy_gate_requires_real_booleans(self):
        with self.assertRaises(ValueError):
            core.deployment_gate(
                0.05,
                0.05,
                "privacy failed",
                "no oversight",
            )

    def test_legacy_gate_still_works_for_boolean_inputs(self):
        self.assertTrue(
            core.deployment_gate(
                0.05,
                0.05,
                True,
                True,
            )
        )


if __name__ == "__main__":
    unittest.main()
