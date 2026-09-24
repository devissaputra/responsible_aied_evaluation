import math
import random
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from numbers import Real


DECISIONS = {"PASS", "CONDITIONAL", "BLOCK", "NOT_EVALUABLE"}
RISK_STATUSES = {"open", "mitigated", "accepted"}


def _finite_number(value, name):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be numeric")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _unit_interval(value, name):
    value = _finite_number(value, name)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    return value


def _positive_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def _text(value, name, *, optional=False):
    if value is None and optional:
        return None
    if not isinstance(value, str) or not value.strip():
        if optional:
            raise ValueError(f"{name} must be a non-empty string or None")
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _bool(value, name):
    if not isinstance(value, bool):
        raise ValueError(f"{name} must be boolean")
    return value


def _binary(value, name):
    if isinstance(value, bool):
        value = int(value)
    if value not in (0, 1):
        raise ValueError(f"{name} must be 0 or 1")
    return int(value)


@dataclass(frozen=True)
class EvaluationRecord:
    case_id: str
    probability: float
    outcome: int
    group: str
    intersectional_group: str | None = None

    def __post_init__(self):
        object.__setattr__(self, "case_id", _text(self.case_id, "case_id"))
        object.__setattr__(
            self,
            "probability",
            _unit_interval(self.probability, "probability"),
        )
        object.__setattr__(self, "outcome", _binary(self.outcome, "outcome"))
        object.__setattr__(self, "group", _text(self.group, "group"))
        if self.intersectional_group is not None:
            object.__setattr__(
                self,
                "intersectional_group",
                _text(
                    self.intersectional_group,
                    "intersectional_group",
                    optional=True,
                ),
            )


@dataclass(frozen=True)
class GovernanceReview:
    privacy_reviewed: bool
    accessibility_reviewed: bool
    human_oversight_defined: bool
    appeal_path_defined: bool
    rollback_plan_defined: bool
    monitoring_plan_defined: bool
    decision_owner: str
    privacy_evidence: str | None = None
    accessibility_evidence: str | None = None
    human_oversight_owner: str | None = None
    appeal_path: str | None = None
    rollback_owner: str | None = None
    monitoring_plan: str | None = None

    def __post_init__(self):
        for name in (
            "privacy_reviewed",
            "accessibility_reviewed",
            "human_oversight_defined",
            "appeal_path_defined",
            "rollback_plan_defined",
            "monitoring_plan_defined",
        ):
            object.__setattr__(self, name, _bool(getattr(self, name), name))
        object.__setattr__(
            self,
            "decision_owner",
            _text(self.decision_owner, "decision_owner"),
        )
        for name in (
            "privacy_evidence",
            "accessibility_evidence",
            "human_oversight_owner",
            "appeal_path",
            "rollback_owner",
            "monitoring_plan",
        ):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(
                    self,
                    name,
                    _text(value, name, optional=True),
                )


@dataclass(frozen=True)
class RiskItem:
    risk_id: str
    description: str
    severity: int
    likelihood: int
    mitigation: str
    owner: str | None = None
    status: str = "open"

    def __post_init__(self):
        object.__setattr__(self, "risk_id", _text(self.risk_id, "risk_id"))
        object.__setattr__(
            self,
            "description",
            _text(self.description, "description"),
        )
        if (
            isinstance(self.severity, bool)
            or not isinstance(self.severity, int)
            or not 1 <= self.severity <= 5
        ):
            raise ValueError("severity must be an integer from 1 to 5")
        if (
            isinstance(self.likelihood, bool)
            or not isinstance(self.likelihood, int)
            or not 1 <= self.likelihood <= 5
        ):
            raise ValueError("likelihood must be an integer from 1 to 5")
        object.__setattr__(
            self,
            "mitigation",
            _text(self.mitigation, "mitigation"),
        )
        if self.owner is not None:
            object.__setattr__(
                self,
                "owner",
                _text(self.owner, "owner", optional=True),
            )
        if self.status not in RISK_STATUSES:
            raise ValueError(
                f"status must be one of {sorted(RISK_STATUSES)}"
            )

    @property
    def risk_score(self):
        return self.severity * self.likelihood


@dataclass(frozen=True)
class DecisionConfig:
    """Study-specific thresholds supplied by the evaluator."""

    probability_threshold: float
    max_ece: float
    max_brier: float
    max_selection_rate_gap: float
    max_tpr_gap: float
    max_fpr_gap: float
    min_group_size: int
    max_open_risk_score: int

    def __post_init__(self):
        for name in (
            "probability_threshold",
            "max_ece",
            "max_brier",
            "max_selection_rate_gap",
            "max_tpr_gap",
            "max_fpr_gap",
        ):
            object.__setattr__(
                self,
                name,
                _unit_interval(getattr(self, name), name),
            )
        _positive_int(self.min_group_size, "min_group_size")
        if (
            isinstance(self.max_open_risk_score, bool)
            or not isinstance(self.max_open_risk_score, int)
            or not 1 <= self.max_open_risk_score <= 25
        ):
            raise ValueError(
                "max_open_risk_score must be an integer from 1 to 25"
            )


def _validate_records(records):
    if not isinstance(records, Sequence) or isinstance(records, (str, bytes)):
        raise ValueError("records must be a sequence")
    if not records:
        raise ValueError("records must not be empty")
    if not all(isinstance(record, EvaluationRecord) for record in records):
        raise ValueError("records must contain EvaluationRecord objects")
    ids = [record.case_id for record in records]
    if len(ids) != len(set(ids)):
        raise ValueError("case_id values must be unique")


def predictions_at_threshold(records, threshold=0.5):
    _validate_records(records)
    threshold = _unit_interval(threshold, "threshold")
    return [
        1 if record.probability >= threshold else 0
        for record in records
    ]


def confusion_metrics(predictions, outcomes):
    if (
        not isinstance(predictions, Sequence)
        or isinstance(predictions, (str, bytes))
        or not isinstance(outcomes, Sequence)
        or isinstance(outcomes, (str, bytes))
        or not predictions
        or len(predictions) != len(outcomes)
    ):
        raise ValueError(
            "predictions and outcomes must be equal non-empty sequences"
        )
    predictions = [_binary(value, "prediction") for value in predictions]
    outcomes = [_binary(value, "outcome") for value in outcomes]

    tp = sum(p == 1 and y == 1 for p, y in zip(predictions, outcomes))
    tn = sum(p == 0 and y == 0 for p, y in zip(predictions, outcomes))
    fp = sum(p == 1 and y == 0 for p, y in zip(predictions, outcomes))
    fn = sum(p == 0 and y == 1 for p, y in zip(predictions, outcomes))
    total = len(predictions)

    def ratio(num, den):
        return num / den if den else None

    return {
        "n": total,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "accuracy": (tp + tn) / total,
        "precision": ratio(tp, tp + fp),
        "recall_tpr": ratio(tp, tp + fn),
        "specificity_tnr": ratio(tn, tn + fp),
        "fpr": ratio(fp, fp + tn),
        "fnr": ratio(fn, fn + tp),
        "selection_rate": (tp + fp) / total,
    }


def calibration_bins(probs, outcomes, bins=10):
    if (
        not isinstance(probs, Sequence)
        or isinstance(probs, (str, bytes))
        or not isinstance(outcomes, Sequence)
        or isinstance(outcomes, (str, bytes))
        or not probs
        or len(probs) != len(outcomes)
    ):
        raise ValueError(
            "probs and outcomes must be equal non-empty sequences"
        )
    bins = _positive_int(bins, "bins")
    probs = [_unit_interval(value, "probability") for value in probs]
    outcomes = [_binary(value, "outcome") for value in outcomes]

    rows = []
    for index in range(bins):
        lower = index / bins
        upper = (index + 1) / bins
        members = [
            position
            for position, probability in enumerate(probs)
            if (
                lower <= probability < upper
                or (
                    index == bins - 1
                    and probability == 1.0
                )
            )
        ]
        if not members:
            continue
        mean_probability = (
            sum(probs[position] for position in members)
            / len(members)
        )
        outcome_rate = (
            sum(outcomes[position] for position in members)
            / len(members)
        )
        rows.append(
            {
                "bin": index,
                "lower": lower,
                "upper": upper,
                "count": len(members),
                "mean_probability": mean_probability,
                "outcome_rate": outcome_rate,
                "absolute_gap": abs(
                    mean_probability - outcome_rate
                ),
            }
        )
    return rows


def expected_calibration_error(probs, outcomes, bins=10):
    rows = calibration_bins(probs, outcomes, bins=bins)
    total = sum(row["count"] for row in rows)
    return sum(
        row["count"] / total * row["absolute_gap"]
        for row in rows
    )


def maximum_calibration_error(probs, outcomes, bins=10):
    rows = calibration_bins(probs, outcomes, bins=bins)
    return max(row["absolute_gap"] for row in rows)


def brier_score(probs, outcomes):
    if (
        not isinstance(probs, Sequence)
        or isinstance(probs, (str, bytes))
        or not isinstance(outcomes, Sequence)
        or isinstance(outcomes, (str, bytes))
        or not probs
        or len(probs) != len(outcomes)
    ):
        raise ValueError(
            "probs and outcomes must be equal non-empty sequences"
        )
    probs = [_unit_interval(value, "probability") for value in probs]
    outcomes = [_binary(value, "outcome") for value in outcomes]
    return sum(
        (probability - outcome) ** 2
        for probability, outcome in zip(probs, outcomes)
    ) / len(probs)


def _gap(values):
    valid = [value for value in values if value is not None]
    if len(valid) < 2:
        return None
    return max(valid) - min(valid)


def group_performance(
    records,
    *,
    threshold=0.5,
    group_field="group",
    min_group_size=5,
):
    _validate_records(records)
    threshold = _unit_interval(threshold, "threshold")
    min_group_size = _positive_int(
        min_group_size,
        "min_group_size",
    )
    if group_field not in {"group", "intersectional_group"}:
        raise ValueError(
            "group_field must be 'group' or 'intersectional_group'"
        )

    grouped = {}
    for record in records:
        label = getattr(record, group_field)
        if label is None:
            continue
        grouped.setdefault(label, []).append(record)

    rows = {}
    warnings = []
    for label in sorted(grouped, key=str):
        subset = grouped[label]
        predictions = predictions_at_threshold(
            subset,
            threshold,
        )
        metrics = confusion_metrics(
            predictions,
            [record.outcome for record in subset],
        )
        rows[label] = metrics
        if len(subset) < min_group_size:
            warnings.append(
                f"group {label!r} has n={len(subset)} below "
                f"min_group_size={min_group_size}"
            )

    if len(rows) < 2:
        status = "not_evaluable"
        reason = "fewer_than_two_groups"
    else:
        status = "scored"
        reason = None

    return {
        "status": status,
        "reason": reason,
        "group_field": group_field,
        "groups": rows,
        "warnings": warnings,
    }


def fairness_report(
    records,
    *,
    threshold=0.5,
    group_field="group",
    min_group_size=5,
):
    performance = group_performance(
        records,
        threshold=threshold,
        group_field=group_field,
        min_group_size=min_group_size,
    )
    if performance["status"] != "scored":
        return {
            **performance,
            "selection_rate_gap": None,
            "tpr_gap": None,
            "fpr_gap": None,
            "fnr_gap": None,
            "accuracy_gap": None,
            "precision_gap": None,
            "equalized_odds_gap": None,
        }

    rows = list(performance["groups"].values())
    selection_gap = _gap(
        [row["selection_rate"] for row in rows]
    )
    tpr_gap = _gap([row["recall_tpr"] for row in rows])
    fpr_gap = _gap([row["fpr"] for row in rows])
    fnr_gap = _gap([row["fnr"] for row in rows])
    accuracy_gap = _gap([row["accuracy"] for row in rows])
    precision_gap = _gap([row["precision"] for row in rows])

    equalized_odds_candidates = [
        value
        for value in (tpr_gap, fpr_gap)
        if value is not None
    ]
    equalized_odds_gap = (
        max(equalized_odds_candidates)
        if equalized_odds_candidates
        else None
    )

    return {
        **performance,
        "selection_rate_gap": selection_gap,
        "tpr_gap": tpr_gap,
        "fpr_gap": fpr_gap,
        "fnr_gap": fnr_gap,
        "accuracy_gap": accuracy_gap,
        "precision_gap": precision_gap,
        "equalized_odds_gap": equalized_odds_gap,
    }


def demographic_parity_difference(
    predictions,
    groups,
    positive=1,
):
    if (
        not isinstance(predictions, Sequence)
        or isinstance(predictions, (str, bytes))
        or not isinstance(groups, Sequence)
        or isinstance(groups, (str, bytes))
        or not predictions
        or len(predictions) != len(groups)
    ):
        raise ValueError(
            "predictions and groups must be non-empty and have equal length"
        )
    unique_groups = sorted(set(groups), key=str)
    if len(unique_groups) < 2:
        raise ValueError(
            "demographic parity requires at least two groups"
        )
    rates = []
    for group in unique_groups:
        values = [
            prediction
            for prediction, label in zip(predictions, groups)
            if label == group
        ]
        rates.append(
            sum(value == positive for value in values)
            / len(values)
        )
    return max(rates) - min(rates)


def group_calibration_report(
    records,
    *,
    bins=5,
    group_field="group",
    min_group_size=5,
):
    _validate_records(records)
    bins = _positive_int(bins, "bins")
    min_group_size = _positive_int(
        min_group_size,
        "min_group_size",
    )
    if group_field not in {"group", "intersectional_group"}:
        raise ValueError(
            "group_field must be 'group' or 'intersectional_group'"
        )

    grouped = {}
    for record in records:
        label = getattr(record, group_field)
        if label is None:
            continue
        grouped.setdefault(label, []).append(record)

    rows = {}
    warnings = []
    for label in sorted(grouped, key=str):
        subset = grouped[label]
        probs = [record.probability for record in subset]
        outcomes = [record.outcome for record in subset]
        rows[label] = {
            "n": len(subset),
            "ece": expected_calibration_error(
                probs,
                outcomes,
                bins=bins,
            ),
            "brier": brier_score(probs, outcomes),
            "bins": calibration_bins(
                probs,
                outcomes,
                bins=bins,
            ),
        }
        if len(subset) < min_group_size:
            warnings.append(
                f"group {label!r} has n={len(subset)} below "
                f"min_group_size={min_group_size}"
            )

    if len(rows) < 2:
        status = "not_evaluable"
        reason = "fewer_than_two_groups"
        ece_gap = None
        brier_gap = None
    else:
        status = "scored"
        reason = None
        ece_gap = _gap([row["ece"] for row in rows.values()])
        brier_gap = _gap(
            [row["brier"] for row in rows.values()]
        )

    return {
        "status": status,
        "reason": reason,
        "group_field": group_field,
        "groups": rows,
        "ece_gap": ece_gap,
        "brier_gap": brier_gap,
        "warnings": warnings,
    }


def _metric_from_records(records, metric, threshold):
    probs = [record.probability for record in records]
    outcomes = [record.outcome for record in records]
    predictions = predictions_at_threshold(records, threshold)

    if metric == "accuracy":
        return confusion_metrics(
            predictions,
            outcomes,
        )["accuracy"]
    if metric == "brier":
        return brier_score(probs, outcomes)
    if metric == "ece":
        return expected_calibration_error(
            probs,
            outcomes,
            bins=5,
        )
    if metric in {
        "selection_rate_gap",
        "tpr_gap",
        "fpr_gap",
    }:
        report = fairness_report(
            records,
            threshold=threshold,
            min_group_size=1,
        )
        if report["status"] != "scored":
            return None
        return report[metric]
    raise ValueError(f"unsupported metric: {metric}")


def bootstrap_interval(
    records,
    metric,
    *,
    threshold=0.5,
    n_resamples=500,
    seed=7,
    alpha=0.05,
):
    _validate_records(records)
    threshold = _unit_interval(threshold, "threshold")
    n_resamples = _positive_int(n_resamples, "n_resamples")
    alpha = _finite_number(alpha, "alpha")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be between 0 and 1")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be an integer")

    point = _metric_from_records(records, metric, threshold)
    if point is None:
        return {
            "status": "not_evaluable",
            "metric": metric,
            "point": None,
            "lower": None,
            "upper": None,
        }

    rng = random.Random(seed)
    values = []
    for _ in range(n_resamples):
        sample = [
            records[rng.randrange(len(records))]
            for _ in range(len(records))
        ]
        # Preserve duplicate draws while making case IDs unique.
        sample = [
            EvaluationRecord(
                case_id=f"boot-{index}",
                probability=record.probability,
                outcome=record.outcome,
                group=record.group,
                intersectional_group=record.intersectional_group,
            )
            for index, record in enumerate(sample)
        ]
        value = _metric_from_records(sample, metric, threshold)
        if value is not None:
            values.append(value)

    if not values:
        return {
            "status": "not_evaluable",
            "metric": metric,
            "point": point,
            "lower": None,
            "upper": None,
        }

    values.sort()

    def quantile(q):
        position = q * (len(values) - 1)
        lower = int(math.floor(position))
        upper = int(math.ceil(position))
        if lower == upper:
            return values[lower]
        weight = position - lower
        return (
            values[lower] * (1 - weight)
            + values[upper] * weight
        )

    return {
        "status": "scored",
        "metric": metric,
        "point": point,
        "lower": quantile(alpha / 2),
        "upper": quantile(1 - alpha / 2),
        "resamples_used": len(values),
    }


def threshold_sensitivity(
    records,
    thresholds=(0.3, 0.5, 0.7),
    *,
    min_group_size=5,
):
    _validate_records(records)
    if (
        not isinstance(thresholds, Sequence)
        or isinstance(thresholds, (str, bytes))
        or not thresholds
    ):
        raise ValueError(
            "thresholds must be a non-empty sequence"
        )
    rows = []
    outcomes = [record.outcome for record in records]
    for threshold in thresholds:
        threshold = _unit_interval(threshold, "threshold")
        predictions = predictions_at_threshold(
            records,
            threshold,
        )
        performance = confusion_metrics(
            predictions,
            outcomes,
        )
        fairness = fairness_report(
            records,
            threshold=threshold,
            min_group_size=min_group_size,
        )
        rows.append(
            {
                "threshold": threshold,
                "accuracy": performance["accuracy"],
                "selection_rate": performance["selection_rate"],
                "selection_rate_gap": fairness[
                    "selection_rate_gap"
                ],
                "tpr_gap": fairness["tpr_gap"],
                "fpr_gap": fairness["fpr_gap"],
                "fairness_status": fairness["status"],
            }
        )
    return rows


def compare_scenarios(
    baseline_records,
    shifted_records,
    *,
    threshold=0.5,
    min_group_size=5,
):
    _validate_records(baseline_records)
    _validate_records(shifted_records)
    threshold = _unit_interval(threshold, "threshold")

    def summary(records):
        probs = [record.probability for record in records]
        outcomes = [record.outcome for record in records]
        predictions = predictions_at_threshold(
            records,
            threshold,
        )
        performance = confusion_metrics(
            predictions,
            outcomes,
        )
        fairness = fairness_report(
            records,
            threshold=threshold,
            min_group_size=min_group_size,
        )
        return {
            "accuracy": performance["accuracy"],
            "brier": brier_score(probs, outcomes),
            "ece": expected_calibration_error(
                probs,
                outcomes,
                bins=5,
            ),
            "selection_rate_gap": fairness[
                "selection_rate_gap"
            ],
            "tpr_gap": fairness["tpr_gap"],
            "fpr_gap": fairness["fpr_gap"],
        }

    baseline = summary(baseline_records)
    shifted = summary(shifted_records)
    delta = {}
    for name in baseline:
        if (
            baseline[name] is None
            or shifted[name] is None
        ):
            delta[name] = None
        else:
            delta[name] = shifted[name] - baseline[name]
    return {
        "baseline": baseline,
        "shifted": shifted,
        "delta": delta,
    }


def governance_report(review):
    if not isinstance(review, GovernanceReview):
        raise ValueError(
            "review must be a GovernanceReview"
        )
    checks = {
        "privacy": (
            review.privacy_reviewed
            and review.privacy_evidence is not None
        ),
        "accessibility": (
            review.accessibility_reviewed
            and review.accessibility_evidence is not None
        ),
        "human_oversight": (
            review.human_oversight_defined
            and review.human_oversight_owner is not None
        ),
        "appeal_path": (
            review.appeal_path_defined
            and review.appeal_path is not None
        ),
        "rollback": (
            review.rollback_plan_defined
            and review.rollback_owner is not None
        ),
        "monitoring": (
            review.monitoring_plan_defined
            and review.monitoring_plan is not None
        ),
    }
    failed = [
        name
        for name, passed in checks.items()
        if not passed
    ]
    return {
        "checks": checks,
        "failed_checks": failed,
        "complete": not failed,
        "decision_owner": review.decision_owner,
    }


def risk_register_summary(risks):
    if not isinstance(risks, Sequence) or isinstance(
        risks,
        (str, bytes),
    ):
        raise ValueError("risks must be a sequence")
    if not all(isinstance(risk, RiskItem) for risk in risks):
        raise ValueError(
            "risks must contain RiskItem objects"
        )
    rows = [
        {
            "risk_id": risk.risk_id,
            "description": risk.description,
            "severity": risk.severity,
            "likelihood": risk.likelihood,
            "risk_score": risk.risk_score,
            "mitigation": risk.mitigation,
            "owner": risk.owner,
            "status": risk.status,
        }
        for risk in risks
    ]
    rows.sort(
        key=lambda row: (-row["risk_score"], row["risk_id"])
    )
    open_scores = [
        row["risk_score"]
        for row in rows
        if row["status"] == "open"
    ]
    return {
        "risks": rows,
        "open_count": sum(
            row["status"] == "open"
            for row in rows
        ),
        "highest_open_risk_score": (
            max(open_scores)
            if open_scores
            else None
        ),
    }


def responsible_aied_decision(
    records,
    governance,
    risks,
    config,
):
    """Return a transparent study-specific decision report."""
    _validate_records(records)
    if not isinstance(config, DecisionConfig):
        raise ValueError("config must be a DecisionConfig")

    probs = [record.probability for record in records]
    outcomes = [record.outcome for record in records]
    fairness = fairness_report(
        records,
        threshold=config.probability_threshold,
        min_group_size=config.min_group_size,
    )
    calibration = {
        "ece": expected_calibration_error(
            probs,
            outcomes,
            bins=5,
        ),
        "brier": brier_score(probs, outcomes),
        "bins": calibration_bins(
            probs,
            outcomes,
            bins=5,
        ),
    }
    governance_result = governance_report(governance)
    risk_result = risk_register_summary(risks)

    blocking_reasons = []
    warnings = []
    mitigations = []

    if fairness["status"] != "scored":
        return {
            "decision": "NOT_EVALUABLE",
            "blocking_reasons": [
                "fairness comparison requires at least two evaluable groups"
            ],
            "warnings": fairness["warnings"],
            "required_mitigations": [
                "collect or define a valid comparison population before deployment review"
            ],
            "fairness": fairness,
            "calibration": calibration,
            "governance": governance_result,
            "risks": risk_result,
            "config": config,
        }

    if calibration["ece"] > config.max_ece:
        blocking_reasons.append(
            "expected calibration error exceeds the study-specific limit"
        )
        mitigations.append(
            "recalibrate or revise the model and repeat calibration evaluation"
        )
    if calibration["brier"] > config.max_brier:
        blocking_reasons.append(
            "Brier score exceeds the study-specific limit"
        )
        mitigations.append(
            "improve probabilistic performance and re-evaluate"
        )

    for metric_name, limit in (
        (
            "selection_rate_gap",
            config.max_selection_rate_gap,
        ),
        ("tpr_gap", config.max_tpr_gap),
        ("fpr_gap", config.max_fpr_gap),
    ):
        value = fairness[metric_name]
        if value is None:
            warnings.append(
                f"{metric_name} is not evaluable for all groups"
            )
        elif value > limit:
            blocking_reasons.append(
                f"{metric_name} exceeds the study-specific limit"
            )
            mitigations.append(
                f"investigate causes of {metric_name} and evaluate mitigation"
            )

    if fairness["warnings"]:
        warnings.extend(fairness["warnings"])
        mitigations.append(
            "increase subgroup evidence or justify why small-group estimates are usable"
        )

    if not governance_result["complete"]:
        blocking_reasons.append(
            "required governance evidence is incomplete"
        )
        for check in governance_result["failed_checks"]:
            mitigations.append(
                f"complete documented {check} evidence"
            )

    highest_open = risk_result["highest_open_risk_score"]
    if (
        highest_open is not None
        and highest_open > config.max_open_risk_score
    ):
        blocking_reasons.append(
            "open risk exceeds the study-specific risk tolerance"
        )
        mitigations.append(
            "mitigate, formally accept, or re-scope the highest open risk"
        )

    if blocking_reasons:
        decision = "BLOCK"
    elif warnings:
        decision = "CONDITIONAL"
    else:
        decision = "PASS"

    assert decision in DECISIONS
    return {
        "decision": decision,
        "blocking_reasons": sorted(set(blocking_reasons)),
        "warnings": sorted(set(warnings)),
        "required_mitigations": sorted(set(mitigations)),
        "fairness": fairness,
        "calibration": calibration,
        "governance": governance_result,
        "risks": risk_result,
        "config": config,
    }


# Backward-compatible legacy gate. New work should use
# responsible_aied_decision() with an explicit DecisionConfig.
def deployment_gate(
    ece,
    fairness_gap,
    privacy_reviewed,
    human_oversight,
):
    ece = _unit_interval(ece, "ece")
    fairness_gap = _unit_interval(
        fairness_gap,
        "fairness_gap",
    )
    _bool(privacy_reviewed, "privacy_reviewed")
    _bool(human_oversight, "human_oversight")
    return (
        ece <= 0.10
        and fairness_gap <= 0.10
        and privacy_reviewed
        and human_oversight
    )
