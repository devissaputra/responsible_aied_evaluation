import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from responsible_aied_evaluation.core import (
    DecisionConfig,
    EvaluationRecord,
    GovernanceReview,
    RiskItem,
    bootstrap_interval,
    compare_scenarios,
    confusion_metrics,
    expected_calibration_error,
    brier_score,
    fairness_report,
    group_calibration_report,
    predictions_at_threshold,
    responsible_aied_decision,
    threshold_sensitivity,
)


def as_bool(value):
    lowered = value.strip().lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    raise ValueError(f"invalid boolean: {value}")


def load_records():
    grouped = {"baseline": [], "shifted": []}
    with (ROOT / "data" / "evaluation.csv").open(
        encoding="utf-8",
        newline="",
    ) as handle:
        for row in csv.DictReader(handle):
            grouped[row["scenario"]].append(
                EvaluationRecord(
                    case_id=row["case_id"],
                    probability=float(row["probability"]),
                    outcome=int(row["outcome"]),
                    group=row["group"],
                    intersectional_group=row[
                        "intersectional_group"
                    ],
                )
            )
    return grouped


def load_governance():
    with (ROOT / "data" / "governance.csv").open(
        encoding="utf-8",
        newline="",
    ) as handle:
        row = next(csv.DictReader(handle))
    return GovernanceReview(
        privacy_reviewed=as_bool(row["privacy_reviewed"]),
        accessibility_reviewed=as_bool(
            row["accessibility_reviewed"]
        ),
        human_oversight_defined=as_bool(
            row["human_oversight_defined"]
        ),
        appeal_path_defined=as_bool(
            row["appeal_path_defined"]
        ),
        rollback_plan_defined=as_bool(
            row["rollback_plan_defined"]
        ),
        monitoring_plan_defined=as_bool(
            row["monitoring_plan_defined"]
        ),
        decision_owner=row["decision_owner"],
        privacy_evidence=row["privacy_evidence"],
        accessibility_evidence=row[
            "accessibility_evidence"
        ],
        human_oversight_owner=row[
            "human_oversight_owner"
        ],
        appeal_path=row["appeal_path"],
        rollback_owner=row["rollback_owner"],
        monitoring_plan=row["monitoring_plan"],
    )


def load_risks():
    values = []
    with (ROOT / "data" / "risks.csv").open(
        encoding="utf-8",
        newline="",
    ) as handle:
        for row in csv.DictReader(handle):
            values.append(
                RiskItem(
                    risk_id=row["risk_id"],
                    description=row["description"],
                    severity=int(row["severity"]),
                    likelihood=int(row["likelihood"]),
                    mitigation=row["mitigation"],
                    owner=row["owner"],
                    status=row["status"],
                )
            )
    return values


def load_config():
    values = {}
    with (
        ROOT / "data" / "decision_thresholds.csv"
    ).open(
        encoding="utf-8",
        newline="",
    ) as handle:
        for row in csv.DictReader(handle):
            values[row["field"]] = row["value"]
    return DecisionConfig(
        probability_threshold=float(
            values["probability_threshold"]
        ),
        max_ece=float(values["max_ece"]),
        max_brier=float(values["max_brier"]),
        max_selection_rate_gap=float(
            values["max_selection_rate_gap"]
        ),
        max_tpr_gap=float(values["max_tpr_gap"]),
        max_fpr_gap=float(values["max_fpr_gap"]),
        min_group_size=int(values["min_group_size"]),
        max_open_risk_score=int(
            values["max_open_risk_score"]
        ),
    )


scenarios = load_records()
baseline = scenarios["baseline"]
shifted = scenarios["shifted"]
config = load_config()
governance = load_governance()
risks = load_risks()

predictions = predictions_at_threshold(
    baseline,
    config.probability_threshold,
)
performance = confusion_metrics(
    predictions,
    [record.outcome for record in baseline],
)
fairness = fairness_report(
    baseline,
    threshold=config.probability_threshold,
    min_group_size=config.min_group_size,
)
calibration = {
    "ece": expected_calibration_error(
        [record.probability for record in baseline],
        [record.outcome for record in baseline],
        bins=5,
    ),
    "brier": brier_score(
        [record.probability for record in baseline],
        [record.outcome for record in baseline],
    ),
}
group_calibration = group_calibration_report(
    baseline,
    bins=4,
    min_group_size=config.min_group_size,
)
uncertainty = bootstrap_interval(
    baseline,
    "tpr_gap",
    threshold=config.probability_threshold,
    n_resamples=200,
    seed=7,
)
sensitivity = threshold_sensitivity(
    baseline,
    thresholds=(0.4, 0.5, 0.6),
    min_group_size=config.min_group_size,
)
shift = compare_scenarios(
    baseline,
    shifted,
    threshold=config.probability_threshold,
    min_group_size=config.min_group_size,
)
decision = responsible_aied_decision(
    baseline,
    governance,
    risks,
    config,
)

print("Responsible AIED Evaluation Toolkit synthetic demo")
print()
print("Overall performance:")
print(performance)
print("\nCalibration:")
print(calibration)
print("\nFairness:")
print(
    {
        "selection_rate_gap": fairness[
            "selection_rate_gap"
        ],
        "tpr_gap": fairness["tpr_gap"],
        "fpr_gap": fairness["fpr_gap"],
        "equalized_odds_gap": fairness[
            "equalized_odds_gap"
        ],
        "warnings": fairness["warnings"],
    }
)
print("\nGroup calibration:")
print(
    {
        "ece_gap": group_calibration["ece_gap"],
        "brier_gap": group_calibration["brier_gap"],
        "warnings": group_calibration["warnings"],
    }
)
print("\nBootstrap uncertainty for TPR gap:")
print(uncertainty)
print("\nThreshold sensitivity:")
for row in sensitivity:
    print(row)
print("\nBaseline versus shifted scenario:")
print(shift)
print("\nDecision report:")
print(
    {
        "decision": decision["decision"],
        "blocking_reasons": decision[
            "blocking_reasons"
        ],
        "warnings": decision["warnings"],
        "required_mitigations": decision[
            "required_mitigations"
        ],
        "failed_governance_checks": decision[
            "governance"
        ]["failed_checks"],
        "highest_open_risk_score": decision[
            "risks"
        ]["highest_open_risk_score"],
    }
)

print(
    "\nNote: all records, groups, governance evidence, risks, "
    "thresholds, and shift patterns are synthetic. The decision is a "
    "software demonstration using explicit study-specific thresholds, "
    "not a universal statement that an educational AI system is safe."
)
