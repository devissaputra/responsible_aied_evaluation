# Calculation guide

## Question and evidence

How should a dropout predictor be audited before use?

UCI 697: 4,424 historical student records; 20 retained predictors.

**Status:** RECORDED EXTERNAL-DATA STUDY | full experiment not rerun in this review.

## Design

Exclude post-enrollment and audit-only fields; train/test evaluation, calibration, subgroup support checks and threshold sensitivity.

## Calculation and interpretation

`Brier = mean((p-y)^2); selection gap = max(group rates)-min(group rates).`

No recorded dropout includes enrolled and graduated cases; it is not synonymous with success. Group rates need adequate positive and negative support. An unevaluable group must not be represented as having zero disparity.

## Evidence table

Selected recorded values (units and context shown). Full precision below is for traceability, not a claim of measurement precision.

| Quantity | Value | Unit / meaning | JSON path |
|---|---:|---|---|
| roc_auc | 0.8316010873895621 | unitless | `primary_split.overall.roc_auc` |
| brier | 0.14465658949166413 | unitless | `primary_split.overall.brier` |
| log_loss | 0.4501032086402171 | unitless | `primary_split.overall.log_loss` |
| ece_10 | 0.04134547372176672 | unitless | `primary_split.overall.ece_10` |

Source: [results/uci697_audit.json](results/uci697_audit.json). Values resolve directly from this file when figures are regenerated.

The primary holdout reports ROC-AUC 0.8316 and Brier score 0.1447. Gender diagnostics can be calculated, while international, intersectional, and special-needs audits remain unevaluable under the support rules. Repeated splits and bootstrap checks describe uncertainty, but incomplete governance evidence and the historical dataset prevent a deployment or fairness certification.

## Verification performed in this review

The existing suite requires unavailable dependencies; no full-suite pass is claimed. The complete data/model experiment was not rerun in this review. Stored empirical results were inspected, not independently reproduced from raw data.

The figure-generation check verifies agreement between the selected source values and SVGs. It does not validate the raw dataset, fitted model, identification assumptions, or external generalization.

```bash
python scripts/build_review_figures.py
python scripts/build_review_figures.py --check
```

## Implementation map

Follow these functions to inspect each transformation. Validation helpers and private functions remain visible in the linked modules.

| Function | Purpose / documented behavior |
|---|---|
| [`normalize_target`](scripts/run_uci_study.py#L72) | Inspect the explicit implementation and its callers. |
| [`enrollment_feature_frame`](scripts/run_uci_study.py#L81) | Inspect the explicit implementation and its callers. |
| [`dataset_fingerprint`](scripts/run_uci_study.py#L102) | Inspect the explicit implementation and its callers. |
| [`build_audit_frame`](scripts/run_uci_study.py#L117) | Inspect the explicit implementation and its callers. |
| [`build_model`](scripts/run_uci_study.py#L148) | Inspect the explicit implementation and its callers. |
| [`calibration_slope_intercept`](scripts/run_uci_study.py#L172) | Inspect the explicit implementation and its callers. |
| [`overall_metrics`](scripts/run_uci_study.py#L185) | Inspect the explicit implementation and its callers. |
| [`make_records`](scripts/run_uci_study.py#L240) | Inspect the explicit implementation and its callers. |
| [`group_audit`](scripts/run_uci_study.py#L257) | Inspect the explicit implementation and its callers. |
| [`intersectional_audit`](scripts/run_uci_study.py#L304) | Inspect the explicit implementation and its callers. |
| [`evaluate_split`](scripts/run_uci_study.py#L380) | Inspect the explicit implementation and its callers. |
| [`repeated_split_robustness`](scripts/run_uci_study.py#L469) | Inspect the explicit implementation and its callers. |
| [`training_refit_bootstrap`](scripts/run_uci_study.py#L508) | Inspect the explicit implementation and its callers. |
| [`target_sensitivity`](scripts/run_uci_study.py#L592) | Inspect the explicit implementation and its callers. |
| [`governance_and_risk_context`](scripts/run_uci_study.py#L627) | Inspect the explicit implementation and its callers. |
| [`write_figures`](scripts/run_uci_study.py#L699) | Inspect the explicit implementation and its callers. |
| [`write_summary`](scripts/run_uci_study.py#L816) | Inspect the explicit implementation and its callers. |
| [`main`](scripts/run_uci_study.py#L880) | Inspect the explicit implementation and its callers. |
| [`predictions_at_threshold`](src/responsible_aied_evaluation/core.py#L242) | Inspect the explicit implementation and its callers. |
| [`confusion_metrics`](src/responsible_aied_evaluation/core.py#L251) | Inspect the explicit implementation and its callers. |
| [`calibration_bins`](src/responsible_aied_evaluation/core.py#L291) | Inspect the explicit implementation and its callers. |
| [`expected_calibration_error`](src/responsible_aied_evaluation/core.py#L348) | Inspect the explicit implementation and its callers. |
| [`maximum_calibration_error`](src/responsible_aied_evaluation/core.py#L357) | Inspect the explicit implementation and its callers. |
| [`brier_score`](src/responsible_aied_evaluation/core.py#L362) | Inspect the explicit implementation and its callers. |
| [`group_performance`](src/responsible_aied_evaluation/core.py#L389) | Inspect the explicit implementation and its callers. |
| [`fairness_report`](src/responsible_aied_evaluation/core.py#L446) | Inspect the explicit implementation and its callers. |
| [`demographic_parity_difference`](src/responsible_aied_evaluation/core.py#L501) | Inspect the explicit implementation and its callers. |
| [`group_calibration_report`](src/responsible_aied_evaluation/core.py#L536) | Inspect the explicit implementation and its callers. |
| [`bootstrap_interval`](src/responsible_aied_evaluation/core.py#L631) | Inspect the explicit implementation and its callers. |
| [`threshold_sensitivity`](src/responsible_aied_evaluation/core.py#L748) | Inspect the explicit implementation and its callers. |
| [`compare_scenarios`](src/responsible_aied_evaluation/core.py#L796) | Inspect the explicit implementation and its callers. |
| [`governance_report`](src/responsible_aied_evaluation/core.py#L856) | Inspect the explicit implementation and its callers. |
| [`risk_register_summary`](src/responsible_aied_evaluation/core.py#L900) | Inspect the explicit implementation and its callers. |
| [`configured_evidence_review`](src/responsible_aied_evaluation/core.py#L945) | Apply evaluator-supplied evidence criteria without claiming fairness or deployment readiness. |
| [`risk_score`](src/responsible_aied_evaluation/core.py#L188) | Inspect the explicit implementation and its callers. |
| [`ratio`](src/responsible_aied_evaluation/core.py#L272) | Inspect the explicit implementation and its callers. |
| [`quantile`](src/responsible_aied_evaluation/core.py#L727) | Inspect the explicit implementation and its callers. |
| [`summary`](src/responsible_aied_evaluation/core.py#L807) | Inspect the explicit implementation and its callers. |

## What remains before a stronger research claim

No recorded dropout includes enrolled and graduated cases; it is not synonymous with success. Group rates need adequate positive and negative support. An unevaluable group must not be represented as having zero disparity. A successful software test is not validation of a scientific construct. New experiments should state their split unit, comparator, outcome, uncertainty procedure and failure criteria before examining final test results.
