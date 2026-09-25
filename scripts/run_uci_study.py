from __future__ import annotations

import hashlib
import importlib.metadata
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    balanced_accuracy_score,
    log_loss,
    precision_recall_curve,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from ucimlrepo import fetch_ucirepo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from responsible_aied_evaluation.core import (
    EvaluationRecord,
    GovernanceReview,
    RiskItem,
    brier_score,
    bootstrap_interval,
    confusion_metrics,
    expected_calibration_error,
    fairness_report,
    governance_report,
    group_calibration_report,
    predictions_at_threshold,
    risk_register_summary,
    threshold_sensitivity,
)

SEED = 42
UCI_ID = 697
UCI_DOI = "10.24432/C5MC89"
UCI_LICENSE = "CC BY 4.0"
MIN_GROUP_SIZE = 30
REPEATED_SPLIT_SEEDS = [11, 23, 42, 73, 101, 131, 173, 211, 257, 307]
TRAINING_BOOTSTRAP_ITERATIONS = 200
HOLDOUT_BOOTSTRAP_ITERATIONS = 1000

CONTINUOUS = {
    "Previous qualification (grade)",
    "Admission grade",
    "Age at enrollment",
    "Unemployment rate",
    "Inflation rate",
    "GDP",
}
AUDIT_ONLY_FIELDS = [
    "Gender",
    "Nacionality",
    "International",
    "Educational special needs",
]


def normalize_target(raw: pd.Series) -> pd.Series:
    series = pd.Series(raw).astype(str).str.strip()
    allowed = {"Dropout", "Enrolled", "Graduate"}
    observed = set(series.unique())
    if not observed.issubset(allowed):
        raise ValueError(f"unexpected target labels: {sorted(observed)}")
    return (series == "Dropout").astype(int)


def enrollment_feature_frame(X: pd.DataFrame) -> tuple[pd.DataFrame, list[str], list[str]]:
    forbidden = [
        column
        for column in X.columns
        if "Curricular units 1st sem" in column
        or "Curricular units 2nd sem" in column
    ]
    audit_only = [column for column in AUDIT_ONLY_FIELDS if column in X.columns]
    model = X.drop(columns=forbidden + audit_only).copy()
    leaked = [
        column
        for column in model.columns
        if "Curricular units 1st sem" in column
        or "Curricular units 2nd sem" in column
        or column in AUDIT_ONLY_FIELDS
    ]
    if leaked:
        raise ValueError(f"timing/protected feature leakage detected: {leaked}")
    return model, forbidden, audit_only


def dataset_fingerprint(X: pd.DataFrame, target: pd.Series) -> str:
    combined = X.copy()
    combined["__target__"] = pd.Series(target).astype(str).to_numpy()
    payload = combined.to_csv(index=False, lineterminator="\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _binary_labels(series: pd.Series, mapping: dict[int, str], name: str) -> pd.Series:
    numeric = pd.to_numeric(series, errors="raise").astype(int)
    unknown = sorted(set(numeric.unique()) - set(mapping))
    if unknown:
        raise ValueError(f"unexpected {name} codes: {unknown}")
    return numeric.map(mapping)


def build_audit_frame(X: pd.DataFrame) -> pd.DataFrame:
    required = set(AUDIT_ONLY_FIELDS)
    missing = sorted(required - set(X.columns))
    if missing:
        raise ValueError(f"missing frozen audit fields: {missing}")

    audit = pd.DataFrame(index=X.index)
    audit["gender"] = _binary_labels(
        X["Gender"], {0: "female", 1: "male"}, "Gender"
    )
    audit["international"] = _binary_labels(
        X["International"], {0: "domestic", 1: "international"}, "International"
    )
    audit["special_needs"] = _binary_labels(
        X["Educational special needs"],
        {0: "no_special_needs_flag", 1: "special_needs_flag"},
        "Educational special needs",
    )

    nationality = pd.to_numeric(X["Nacionality"], errors="raise").astype(int)
    audit["nationality_group"] = np.where(
        nationality.eq(1), "portuguese", "non_portuguese"
    )
    audit["gender_x_international"] = (
        audit["gender"].astype(str)
        + "__"
        + audit["international"].astype(str)
    )
    return audit


def build_model(X: pd.DataFrame) -> Pipeline:
    numeric = [column for column in X.columns if column in CONTINUOUS]
    categorical = [column for column in X.columns if column not in numeric]
    preprocess = ColumnTransformer(
        [
            ("continuous", StandardScaler(), numeric),
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
        ]
    )
    return Pipeline(
        [
            ("preprocess", preprocess),
            (
                "model",
                LogisticRegression(
                    max_iter=4000,
                    random_state=SEED,
                    class_weight=None,
                ),
            ),
        ]
    )


def calibration_slope_intercept(probability: np.ndarray, outcome: np.ndarray) -> dict:
    p = np.clip(np.asarray(probability, dtype=float), 1e-6, 1 - 1e-6)
    y = np.asarray(outcome, dtype=int)
    logit = np.log(p / (1 - p)).reshape(-1, 1)
    calibrator = LogisticRegression(C=1e6, max_iter=4000, random_state=SEED)
    calibrator.fit(logit, y)
    return {
        "intercept": float(calibrator.intercept_[0]),
        "slope": float(calibrator.coef_[0, 0]),
        "reference": {"intercept": 0.0, "slope": 1.0},
    }


def overall_metrics(
    probability: np.ndarray,
    outcome: np.ndarray,
    threshold: float = 0.5,
    *,
    include_sample_bootstrap: bool = False,
) -> dict:
    y = np.asarray(outcome, dtype=int)
    p = np.asarray(probability, dtype=float)
    prediction = (p >= threshold).astype(int)
    records = [
        EvaluationRecord(str(i), float(prob), int(label), "all")
        for i, (prob, label) in enumerate(zip(p, y))
    ]
    result = {
        "prevalence": float(np.mean(y)),
        "roc_auc": float(roc_auc_score(y, p)),
        "average_precision": float(average_precision_score(y, p)),
        "brier": float(brier_score(p.tolist(), y.tolist())),
        "log_loss": float(log_loss(y, p, labels=[0, 1])),
        "ece_10": float(expected_calibration_error(p.tolist(), y.tolist(), bins=10)),
        "calibration": calibration_slope_intercept(p, y),
        "balanced_accuracy_at_0_50": float(balanced_accuracy_score(y, prediction)),
        "confusion_at_0_50": confusion_metrics(prediction.tolist(), y.tolist()),
        "reference_threshold": 0.5,
        "threshold_note": "0.50 is a descriptive reference threshold, not an optimized or ethically preferred intervention threshold.",
    }
    if include_sample_bootstrap:
        result["sample_bootstrap"] = {
            metric: bootstrap_interval(
                records,
                metric,
                threshold=threshold,
                n_resamples=HOLDOUT_BOOTSTRAP_ITERATIONS,
                seed=SEED,
            )
            for metric in ["accuracy", "brier", "ece"]
        }
    return result


def make_records(
    indices: np.ndarray,
    probability: np.ndarray,
    outcome: np.ndarray,
    labels: pd.Series,
) -> list[EvaluationRecord]:
    return [
        EvaluationRecord(
            str(int(row_index)),
            float(prob),
            int(label),
            str(labels.loc[row_index]),
        )
        for row_index, prob, label in zip(indices, probability, outcome)
    ]


def group_audit(
    indices: np.ndarray,
    probability: np.ndarray,
    outcome: np.ndarray,
    labels: pd.Series,
    *,
    include_bootstrap: bool = True,
) -> dict:
    records = make_records(indices, probability, outcome, labels)
    fairness = fairness_report(
        records,
        threshold=0.5,
        min_group_size=MIN_GROUP_SIZE,
    )
    calibration = group_calibration_report(
        records,
        bins=5,
        min_group_size=MIN_GROUP_SIZE,
    )
    result = {
        "fairness_metrics": fairness,
        "calibration": calibration,
        "threshold_sensitivity": threshold_sensitivity(
            records,
            [0.30, 0.40, 0.50, 0.60, 0.70],
            min_group_size=MIN_GROUP_SIZE,
        ),
        "interpretation": (
            "Descriptive group audit only. Gaps are computed only across groups meeting "
            f"min_group_size={MIN_GROUP_SIZE}; they are not fairness verdicts."
        ),
    }
    if include_bootstrap:
        result["conditional_holdout_bootstrap"] = {
            metric: bootstrap_interval(
                records,
                metric,
                threshold=0.5,
                n_resamples=HOLDOUT_BOOTSTRAP_ITERATIONS,
                seed=SEED,
                min_group_size=MIN_GROUP_SIZE,
                stratify_by_group=True,
            )
            for metric in ["selection_rate_gap", "tpr_gap", "fpr_gap"]
        }
    return result

def intersectional_audit(
    indices: np.ndarray,
    probability: np.ndarray,
    outcome: np.ndarray,
    audit_frame: pd.DataFrame,
    *,
    include_bootstrap: bool = True,
) -> dict:
    labels = audit_frame["gender_x_international"]
    result = group_audit(
        indices,
        probability,
        outcome,
        labels,
        include_bootstrap=include_bootstrap,
    )
    result["definition"] = "gender x international-status intersection"
    return result

def evaluate_split(
    model_X: pd.DataFrame,
    y: pd.Series,
    audit_frame: pd.DataFrame,
    seed: int,
    *,
    detailed: bool = False,
    include_sample_bootstrap: bool = False,
    include_group_bootstrap: bool = False,
) -> dict:
    indices = np.arange(len(model_X))
    train_idx, test_idx = train_test_split(
        indices,
        test_size=0.20,
        random_state=seed,
        stratify=y,
    )
    model = build_model(model_X.iloc[train_idx])
    model.fit(model_X.iloc[train_idx], y.iloc[train_idx])
    probability = model.predict_proba(model_X.iloc[test_idx])[:, 1]
    y_test = y.iloc[test_idx].to_numpy()

    out = {
        "seed": int(seed),
        "n_train": int(len(train_idx)),
        "n_test": int(len(test_idx)),
        "overall": overall_metrics(
            probability,
            y_test,
            include_sample_bootstrap=include_sample_bootstrap,
        ),
    }
    if detailed:
        out.update(
            {
                "train_indices": train_idx,
                "test_indices": test_idx,
                "probability": probability,
                "y_test": y_test,
                "gender": group_audit(
                    test_idx,
                    probability,
                    y_test,
                    audit_frame["gender"],
                    include_bootstrap=include_group_bootstrap,
                ),
                "international": group_audit(
                    test_idx,
                    probability,
                    y_test,
                    audit_frame["international"],
                    include_bootstrap=include_group_bootstrap,
                ),
                "nationality_group": group_audit(
                    test_idx,
                    probability,
                    y_test,
                    audit_frame["nationality_group"],
                    include_bootstrap=include_group_bootstrap,
                ),
                "special_needs": group_audit(
                    test_idx,
                    probability,
                    y_test,
                    audit_frame["special_needs"],
                    include_bootstrap=include_group_bootstrap,
                ),
                "intersectional_gender_international": intersectional_audit(
                    test_idx,
                    probability,
                    y_test,
                    audit_frame,
                    include_bootstrap=include_group_bootstrap,
                ),
            }
        )
    return out

def _summary(values: list[float]) -> dict:
    array = np.asarray(values, dtype=float)
    return {
        "n": int(len(array)),
        "mean": float(np.mean(array)),
        "sd": float(np.std(array, ddof=1)) if len(array) > 1 else 0.0,
        "min": float(np.min(array)),
        "max": float(np.max(array)),
    }


def repeated_split_robustness(
    model_X: pd.DataFrame,
    y: pd.Series,
    audit_frame: pd.DataFrame,
) -> dict:
    rows = []
    for seed in REPEATED_SPLIT_SEEDS:
        split = evaluate_split(model_X, y, audit_frame, seed, detailed=True)
        row = {
            "seed": seed,
            "roc_auc": split["overall"]["roc_auc"],
            "average_precision": split["overall"]["average_precision"],
            "brier": split["overall"]["brier"],
            "ece_10": split["overall"]["ece_10"],
        }
        for audit_name in ["gender", "international"]:
            fairness = split[audit_name]["fairness_metrics"]
            for metric in ["selection_rate_gap", "tpr_gap", "fpr_gap"]:
                row[f"{audit_name}_{metric}"] = fairness.get(metric)
        rows.append(row)

    summaries = {}
    for key in rows[0]:
        if key == "seed":
            continue
        values = [row[key] for row in rows if row[key] is not None]
        if values:
            summaries[key] = _summary(values)
    return {
        "seeds": REPEATED_SPLIT_SEEDS,
        "rows": rows,
        "summary": summaries,
        "interpretation": (
            "Repeated stratified 80/20 splits quantify split/training sensitivity. "
            "They are robustness evidence, not an external-validation substitute."
        ),
    }


def training_refit_bootstrap(
    model_X: pd.DataFrame,
    y: pd.Series,
    audit_frame: pd.DataFrame,
    train_idx: np.ndarray,
    test_idx: np.ndarray,
) -> dict:
    rng = np.random.default_rng(20260925)
    train_y = y.iloc[train_idx].to_numpy()
    by_class = {
        label: train_idx[train_y == label]
        for label in sorted(np.unique(train_y))
    }
    y_test = y.iloc[test_idx].to_numpy()

    metric_rows = []
    for _ in range(TRAINING_BOOTSTRAP_ITERATIONS):
        sampled_parts = [
            rng.choice(class_indices, size=len(class_indices), replace=True)
            for class_indices in by_class.values()
        ]
        sampled = np.concatenate(sampled_parts)
        rng.shuffle(sampled)

        model = build_model(model_X.iloc[sampled])
        model.fit(model_X.iloc[sampled], y.iloc[sampled])
        probability = model.predict_proba(model_X.iloc[test_idx])[:, 1]
        metrics = overall_metrics(probability, y_test, include_sample_bootstrap=False)

        row = {
            "roc_auc": metrics["roc_auc"],
            "average_precision": metrics["average_precision"],
            "brier": metrics["brier"],
            "ece_10": metrics["ece_10"],
        }
        for audit_name, label_column in [
            ("gender", "gender"),
            ("international", "international"),
        ]:
            fairness = fairness_report(
                make_records(
                    test_idx,
                    probability,
                    y_test,
                    audit_frame[label_column],
                ),
                threshold=0.5,
                min_group_size=MIN_GROUP_SIZE,
            )
            for metric in ["selection_rate_gap", "tpr_gap", "fpr_gap"]:
                row[f"{audit_name}_{metric}"] = fairness.get(metric)
        metric_rows.append(row)

    summary = {}
    for key in metric_rows[0]:
        values = [row[key] for row in metric_rows if row[key] is not None]
        if not values:
            summary[key] = {
                "status": "not_evaluable",
                "n_valid": 0,
                "median": None,
                "lower_95": None,
                "upper_95": None,
            }
            continue
        array = np.asarray(values, dtype=float)
        summary[key] = {
            "status": "scored",
            "n_valid": int(len(array)),
            "median": float(np.median(array)),
            "lower_95": float(np.quantile(array, 0.025)),
            "upper_95": float(np.quantile(array, 0.975)),
        }
    return {
        "method": (
            "Stratified bootstrap of the original training partition with model and "
            "preprocessing refit in every resample; evaluated on the fixed untouched holdout."
        ),
        "iterations": TRAINING_BOOTSTRAP_ITERATIONS,
        "seed": 20260925,
        "summary": summary,
    }


def target_sensitivity(
    X: pd.DataFrame,
    raw_target: pd.Series,
    audit_frame: pd.DataFrame,
) -> dict:
    labels = pd.Series(raw_target).astype(str).str.strip()
    mask = labels.isin(["Dropout", "Graduate"]).to_numpy()
    X_sub = X.loc[mask].reset_index(drop=True)
    audit_sub = audit_frame.loc[mask].reset_index(drop=True)
    y_sub = (labels.loc[mask].reset_index(drop=True) == "Dropout").astype(int)
    model_X, forbidden, audit_only = enrollment_feature_frame(X_sub)
    split = evaluate_split(
        model_X,
        y_sub,
        audit_sub,
        SEED,
        detailed=True,
        include_sample_bootstrap=False,
        include_group_bootstrap=False,
    )
    return {
        "definition": "Dropout versus Graduate only; Enrolled cases excluded as unresolved endpoint sensitivity.",
        "n": int(len(X_sub)),
        "class_counts": {
            "dropout": int(y_sub.sum()),
            "graduate": int((1 - y_sub).sum()),
        },
        "forbidden_post_enrollment_columns": forbidden,
        "audit_only_fields": audit_only,
        "overall": split["overall"],
        "gender": split["gender"],
        "international": split["international"],
    }


def governance_and_risk_context() -> dict:
    review = GovernanceReview(
        privacy_reviewed=False,
        accessibility_reviewed=False,
        human_oversight_defined=False,
        appeal_path_defined=False,
        rollback_plan_defined=False,
        monitoring_plan_defined=False,
        decision_owner="No deployment decision owner: research audit only",
    )
    governance = governance_report(review)

    risks = [
        RiskItem(
            "R1",
            "Historical outcome labels may encode institutional and structural inequities.",
            5,
            3,
            "Treat outputs as descriptive research evidence; require institutional review and external validation before any use.",
        ),
        RiskItem(
            "R2",
            "False-positive dropout flags could stigmatize learners or trigger unnecessary intervention.",
            5,
            3,
            "Do not deploy from this study; prospectively test intervention harms and benefits with human oversight.",
        ),
        RiskItem(
            "R3",
            "The binary primary target combines Enrolled and Graduate as no recorded dropout at the dataset endpoint.",
            4,
            3,
            "Report the endpoint definition and a Dropout-versus-Graduate sensitivity analysis.",
        ),
        RiskItem(
            "R4",
            "Subgroup estimates can be unstable for sparse protected/intersectional groups.",
            4,
            3,
            "Apply minimum evidence thresholds, retain warnings, and avoid gap estimates for under-sized groups.",
        ),
        RiskItem(
            "R5",
            "Single-institution historical data may not transport to other institutions or present-day cohorts.",
            5,
            4,
            "Require external and temporal validation before operational consideration.",
        ),
    ]
    return {
        "deployment_review_executed": False,
        "governance_evidence_gap": governance,
        "risk_register": [
            {
                "risk_id": risk.risk_id,
                "description": risk.description,
                "severity": risk.severity,
                "likelihood": risk.likelihood,
                "risk_score": risk.risk_score,
                "mitigation": risk.mitigation,
                "status": risk.status,
            }
            for risk in risks
        ],
        "risk_summary": risk_register_summary(risks),
        "interpretation": (
            "Governance checks are intentionally incomplete because this repository is a "
            "research audit, not a deployment review. No PASS/BLOCK deployment verdict is produced."
        ),
    }


def write_figures(
    result: dict,
    probability: np.ndarray,
    y_test: np.ndarray,
    test_idx: np.ndarray,
    audit_frame: pd.DataFrame,
) -> None:
    figdir = ROOT / "results" / "figures"
    figdir.mkdir(parents=True, exist_ok=True)

    fpr, tpr, _ = roc_curve(y_test, probability)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(fpr, tpr, label=f"ROC-AUC = {result['primary_split']['overall']['roc_auc']:.3f}")
    ax.plot([0, 1], [0, 1], linestyle="--", linewidth=1)
    ax.set_xlabel("False-positive rate")
    ax.set_ylabel("True-positive rate")
    ax.set_title("Enrollment-time dropout baseline: ROC curve")
    ax.legend()
    fig.tight_layout()
    fig.savefig(figdir / "roc_curve.png", dpi=170)
    plt.close(fig)

    precision, recall, _ = precision_recall_curve(y_test, probability)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(recall, precision, label=f"Average precision = {result['primary_split']['overall']['average_precision']:.3f}")
    ax.axhline(np.mean(y_test), linestyle="--", linewidth=1, label="Dropout prevalence")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Enrollment-time dropout baseline: precision-recall curve")
    ax.legend()
    fig.tight_layout()
    fig.savefig(figdir / "precision_recall_curve.png", dpi=170)
    plt.close(fig)

    prob_true, prob_pred = calibration_curve(y_test, probability, n_bins=10, strategy="uniform")
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(prob_pred, prob_true, marker="o", label="Overall")
    ax.plot([0, 1], [0, 1], linestyle="--", linewidth=1, label="Ideal")
    ax.set_xlabel("Mean predicted probability")
    ax.set_ylabel("Observed dropout rate")
    ax.set_title("Overall probability calibration")
    ax.legend()
    fig.tight_layout()
    fig.savefig(figdir / "overall_calibration.png", dpi=170)
    plt.close(fig)

    for audit_name, column in [
        ("gender", "gender"),
        ("international", "international"),
    ]:
        fig, ax = plt.subplots(figsize=(7, 5))
        labels = audit_frame.loc[test_idx, column]
        for label in sorted(labels.unique()):
            mask = labels.to_numpy() == label
            n_group = int(mask.sum())
            true_rate, pred_rate = calibration_curve(
                y_test[mask], probability[mask], n_bins=5, strategy="uniform"
            )
            suffix = "" if n_group >= MIN_GROUP_SIZE else "; below audit minimum"
            ax.plot(
                pred_rate,
                true_rate,
                marker="o",
                label=f"{label} (n={n_group}{suffix})",
            )
        ax.plot([0, 1], [0, 1], linestyle="--", linewidth=1, label="Ideal")
        ax.set_xlabel("Mean predicted probability")
        ax.set_ylabel("Observed dropout rate")
        ax.set_title(f"Calibration by {audit_name.replace('_', ' ')}")
        ax.legend()
        fig.tight_layout()
        fig.savefig(figdir / f"{audit_name}_calibration.png", dpi=170)
        plt.close(fig)

        rows = result["primary_split"][audit_name]["threshold_sensitivity"]
        fig, ax = plt.subplots(figsize=(7, 5))
        thresholds = [row["threshold"] for row in rows]
        gap_series = {
            metric: [row[metric] for row in rows]
            for metric in ["selection_rate_gap", "tpr_gap", "fpr_gap"]
        }
        if any(any(value is not None for value in values) for values in gap_series.values()):
            for metric, values in gap_series.items():
                ax.plot(thresholds, values, marker="o", label=metric)
            ax.set_xlabel("Reference decision threshold")
            ax.set_ylabel("Absolute group gap")
            ax.set_title(f"Threshold sensitivity: {audit_name.replace('_', ' ')}")
            ax.legend()
        else:
            groups = result["primary_split"][audit_name]["fairness_metrics"]["groups"]
            names = list(groups)
            counts = [groups[name]["n"] for name in names]
            ax.bar(names, counts)
            ax.axhline(MIN_GROUP_SIZE, linestyle="--", linewidth=1)
            ax.set_ylabel("Holdout group size")
            ax.set_title(
                f"{audit_name.replace('_', ' ').title()} gap not evaluable at n={MIN_GROUP_SIZE} minimum"
            )
            ax.tick_params(axis="x", rotation=20)
        fig.tight_layout()
        fig.savefig(figdir / f"{audit_name}_threshold_sensitivity.png", dpi=170)
        plt.close(fig)

    rows = result["repeated_split_robustness"]["rows"]
    fig, ax = plt.subplots(figsize=(7, 5))
    seeds = [row["seed"] for row in rows]
    ax.plot(seeds, [row["roc_auc"] for row in rows], marker="o", label="ROC-AUC")
    ax.plot(seeds, [row["average_precision"] for row in rows], marker="o", label="Average precision")
    ax.set_xlabel("Train/test split seed")
    ax.set_ylabel("Metric")
    ax.set_title("Repeated-split robustness")
    ax.legend()
    fig.tight_layout()
    fig.savefig(figdir / "repeated_split_robustness.png", dpi=170)
    plt.close(fig)


def write_summary(result: dict) -> None:
    primary = result["primary_split"]
    overall = primary["overall"]
    gender = primary["gender"]["fairness_metrics"]
    international = primary["international"]["fairness_metrics"]
    lines = [
        "# Empirical Results Summary",
        "",
        "Generated by scripts/run_uci_study.py; numerical values should not be hand-edited.",
        "",
        "## Dataset and frozen design",
        "",
        f"- UCI dataset: {UCI_ID} — Predict Students' Dropout and Academic Success",
        f"- DOI: {UCI_DOI}",
        f"- Dataset fingerprint SHA-256: {result['dataset']['normalized_sha256']}",
        f"- n: {result['dataset']['n']}; train: {primary['n_train']}; test: {primary['n_test']}",
        f"- Primary endpoint: {result['design']['primary_target']}",
        f"- Predictors after timing/audit-only exclusions: {result['design']['n_model_features']}",
        f"- Excluded post-enrollment columns: {len(result['design']['forbidden_post_enrollment_columns'])}",
        f"- Audit-only fields excluded from prediction: {', '.join(result['design']['audit_only_fields'])}",
        "",
        "## Overall holdout performance",
        "",
        f"- Dropout prevalence: {overall['prevalence']:.4f}",
        f"- ROC-AUC: {overall['roc_auc']:.4f}",
        f"- Average precision: {overall['average_precision']:.4f}",
        f"- Brier score: {overall['brier']:.4f}",
        f"- Log loss: {overall['log_loss']:.4f}",
        f"- ECE-10: {overall['ece_10']:.4f}",
        f"- Calibration intercept: {overall['calibration']['intercept']:.4f}",
        f"- Calibration slope: {overall['calibration']['slope']:.4f}",
        f"- Balanced accuracy at reference threshold 0.50: {overall['balanced_accuracy_at_0_50']:.4f}",
        "",
        "## Group audit at descriptive threshold 0.50",
        "",
        f"- Gender status: {gender['status']}; selection-rate gap: {gender.get('selection_rate_gap')}; TPR gap: {gender.get('tpr_gap')}; FPR gap: {gender.get('fpr_gap')}",
        f"- International-status status: {international['status']}; selection-rate gap: {international.get('selection_rate_gap')}; TPR gap: {international.get('tpr_gap')}; FPR gap: {international.get('fpr_gap')}",
        f"- Intersectional gender x international status: {primary['intersectional_gender_international']['fairness_metrics']['status']}",
        f"- Special-needs audit: {primary['special_needs']['fairness_metrics']['status']}",
        "",
        "## Robustness and uncertainty",
        "",
        f"- Repeated stratified splits: {len(result['repeated_split_robustness']['seeds'])}",
        f"- Training-refit bootstrap iterations: {result['training_refit_bootstrap']['iterations']}",
        f"- Conditional holdout bootstrap iterations per reported metric: {HOLDOUT_BOOTSTRAP_ITERATIONS}",
        f"- Dropout-vs-Graduate sensitivity n: {result['target_sensitivity']['n']}",
        "",
        "## Governance boundary",
        "",
        "The empirical study deliberately produces no deployment PASS/BLOCK verdict. Governance evidence for privacy, accessibility, oversight, appeal, rollback, monitoring and external validation remains incomplete by design.",
        "",
        "## Interpretation boundary",
        "",
        "These results describe one historical Portuguese higher-education dataset and one modeling protocol. They are not a fairness certification, legal determination, causal effect, deployment approval, or evidence that risk-score intervention benefits learners.",
        "",
    ]
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    paper = ROOT / "paper"
    paper.mkdir(exist_ok=True)
    (paper / "results.md").write_text("# Results\n\n" + "\n".join(lines[2:]), encoding="utf-8")


def main() -> None:
    ds = fetch_ucirepo(id=UCI_ID)
    X = ds.data.features.copy().reset_index(drop=True)
    raw_target = ds.data.targets.iloc[:, 0].reset_index(drop=True)
    y = normalize_target(raw_target)
    audit_frame = build_audit_frame(X)
    model_X, forbidden, audit_only = enrollment_feature_frame(X)

    primary = evaluate_split(
        model_X,
        y,
        audit_frame,
        SEED,
        detailed=True,
        include_sample_bootstrap=True,
        include_group_bootstrap=True,
    )
    repeated = repeated_split_robustness(model_X, y, audit_frame)
    refit = training_refit_bootstrap(
        model_X,
        y,
        audit_frame,
        primary["train_indices"],
        primary["test_indices"],
    )

    class_counts = raw_target.astype(str).str.strip().value_counts().to_dict()
    result = {
        "research_bundle": True,
        "status": "complete",
        "dataset": {
            "name": "Predict Students' Dropout and Academic Success",
            "uci_id": UCI_ID,
            "doi": UCI_DOI,
            "license": UCI_LICENSE,
            "n": int(len(X)),
            "original_target_counts": {str(k): int(v) for k, v in class_counts.items()},
            "normalized_sha256": dataset_fingerprint(X, raw_target),
            "fingerprint_definition": (
                "SHA-256 of the normalized feature table plus source target, preserving UCI row and column order."
            ),
        },
        "design": {
            "seed": SEED,
            "primary_target": (
                "Dropout by the dataset observation endpoint versus no recorded dropout "
                "by that endpoint (Enrolled or Graduate)."
            ),
            "target_boundary": (
                "Enrolled is not treated as academic success; it is only grouped with Graduate "
                "for the primary no-recorded-dropout endpoint and is removed in a dedicated sensitivity analysis."
            ),
            "forbidden_post_enrollment_columns": forbidden,
            "audit_only_fields": audit_only,
            "audit_only_rationale": (
                "Gender, nationality, international status, and special-needs status are held out "
                "of prediction and retained for subgroup evaluation. Exclusion of direct attributes "
                "does not prove the remaining feature set is proxy-free."
            ),
            "n_model_features": int(model_X.shape[1]),
            "model": "L2 logistic regression with train-only scaling and one-hot encoding",
            "reference_threshold": 0.5,
            "min_group_size": MIN_GROUP_SIZE,
        },
        "primary_split": {
            key: value
            for key, value in primary.items()
            if key not in {"train_indices", "test_indices", "probability", "y_test"}
        },
        "repeated_split_robustness": repeated,
        "training_refit_bootstrap": refit,
        "target_sensitivity": target_sensitivity(X, raw_target, audit_frame),
        "governance_and_risk": governance_and_risk_context(),
        "environment": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scikit_learn": importlib.metadata.version("scikit-learn"),
            "ucimlrepo": importlib.metadata.version("ucimlrepo"),
            "matplotlib": importlib.metadata.version("matplotlib"),
        },
        "interpretation_boundary": (
            "Responsible-AIED measurement audit only; not fairness certification, "
            "causal inference, legal compliance, beneficial-intervention evidence, or deployment approval."
        ),
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "uci697_audit.json").write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )
    write_figures(
        result,
        primary["probability"],
        primary["y_test"],
        primary["test_indices"],
        audit_frame,
    )
    write_summary(result)
    print(
        json.dumps(
            {
                "status": result["status"],
                "dataset_fingerprint": result["dataset"]["normalized_sha256"],
                "n": result["dataset"]["n"],
                "primary_split": {
                    "n_train": primary["n_train"],
                    "n_test": primary["n_test"],
                    "roc_auc": primary["overall"]["roc_auc"],
                    "average_precision": primary["overall"]["average_precision"],
                    "brier": primary["overall"]["brier"],
                },
                "gender_audit": primary["gender"]["fairness_metrics"]["status"],
                "international_audit": primary["international"]["fairness_metrics"]["status"],
                "intersectional_audit": primary["intersectional_gender_international"]["fairness_metrics"]["status"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
