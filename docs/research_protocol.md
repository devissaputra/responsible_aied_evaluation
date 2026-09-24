# Research protocol

## Project

Responsible AIED Evaluation Toolkit

## Purpose

This toolkit evaluates whether an educational AI system has enough technical, subgroup, uncertainty, risk, and governance evidence to continue to the next stage of review.

It does **not** certify that a system is fair, safe, lawful, ethical, or ready for unrestricted deployment.

## Start with the educational decision

Before choosing metrics, document:

- intended educational use
- affected population
- model output and probability meaning
- intervention triggered by the model
- consequence of a false positive
- consequence of a false negative
- who can override the system
- how learners or instructors can appeal
- monitoring and rollback authority

Metric choice should follow the decision and harm model, not the other way around.

## Research questions

1. How does model performance differ overall and across relevant groups?
2. Are probability estimates calibrated overall and by group?
3. Which fairness definition maps to the educational harm being studied?
4. How uncertain are subgroup disparity estimates?
5. How sensitive are results to decision thresholds?
6. How does performance change under a synthetic or observed distribution shift?
7. Which educational risks remain open?
8. Is governance evidence complete enough for accountable review?

## Technical performance

`confusion_metrics()` reports:

- accuracy
- precision
- recall / true-positive rate
- specificity
- false-positive rate
- false-negative rate
- selection rate
- confusion-matrix counts

Undefined rates return `None` rather than fabricated zero values.

## Fairness analysis

`fairness_report()` reports group-level metrics and gaps for:

- selection rate
- true-positive rate
- false-positive rate
- false-negative rate
- accuracy
- precision
- equalized-odds-style maximum of TPR and FPR gaps

A fairness report is `not_evaluable` when fewer than two groups are available.

Small-group warnings are preserved rather than silently treating unstable estimates as reliable.

The toolkit does not claim that any one fairness metric is universally appropriate.

### Map metrics to harm

Examples:

- If a positive prediction gives beneficial support, TPR/FNR gaps may represent unequal access to needed support.
- If a positive prediction creates an intrusive intervention, FPR gaps may represent unequal unnecessary intervention.
- Selection-rate gaps can describe allocation differences but do not explain whether errors are distributed fairly.

A real study should document this mapping before selecting thresholds.

## Calibration

The toolkit implements:

- calibration-bin tables
- expected calibration error
- maximum calibration error
- Brier score
- group-level ECE and Brier score
- between-group calibration gaps

Calibration-bin tables expose counts, mean predicted probability, observed outcome rate, and absolute gap.

ECE should not be treated as a complete calibration assessment because it depends on binning choices.

## Uncertainty

`bootstrap_interval()` provides a reproducible percentile bootstrap interval for selected metrics.

The current implementation supports:

- accuracy
- Brier score
- ECE
- selection-rate gap
- TPR gap
- FPR gap

The bootstrap is a simple research baseline.

A real study should justify resampling assumptions, confidence level, repeated-measures handling, clustering, and sample size.

## Threshold sensitivity

`threshold_sensitivity()` evaluates multiple probability thresholds and reports:

- accuracy
- selection rate
- selection-rate gap
- TPR gap
- FPR gap

This prevents one arbitrary threshold from being mistaken for a universal system property.

## Robustness / shift comparison

`compare_scenarios()` compares a baseline and shifted scenario on:

- accuracy
- Brier score
- ECE
- selection-rate gap
- TPR gap
- FPR gap

This is a scenario comparison, not a general robustness certification.

Real robustness evaluation may require temporal, institutional, curricular, linguistic, accessibility, or device shifts.

## Governance evidence

`GovernanceReview` requires structured evidence for:

- privacy review
- accessibility review
- human oversight owner
- appeal path
- rollback authority
- monitoring plan
- accountable decision owner

A boolean marked true without corresponding evidence does not pass the governance report.

## Educational risk register

`RiskItem` records:

- risk description
- severity
- likelihood
- mitigation
- owner
- status

The severity × likelihood score is only a prioritization aid.

It is not a universal safety scale.

Potential educational harms include:

- missed support
- unnecessary intervention
- over-support that reduces productive struggle
- stigmatizing labels
- accessibility exclusion
- surveillance burden
- teacher deskilling
- inequitable escalation
- feedback loops that amplify historical inequity

## Decision configuration

`DecisionConfig` contains caller-supplied, study-specific thresholds.

The toolkit intentionally does **not** provide universal ethical deployment thresholds.

A real study should document:

- threshold value
- metric
- affected population
- rationale
- decision owner
- severity of violation
- required mitigation
- uncertainty handling

## Decision states

`responsible_aied_decision()` returns one of:

### PASS

All configured quantitative checks, governance evidence, risk tolerance, and group-evidence requirements pass without warnings.

### CONDITIONAL

No blocking failure exists, but warnings such as small subgroup evidence remain.

### BLOCK

One or more configured metric, governance, or risk conditions fail.

### NOT_EVALUABLE

Required evidence is structurally insufficient, such as having fewer than two comparison groups for the configured fairness review.

Every decision report contains reasons, warnings, and required mitigations.

## Empirical validation plan

A credible study should:

1. freeze the intended use and decision rule
2. define the affected population
3. pre-specify educational harms
4. choose metrics that correspond to those harms
5. define subgroup and intersectional analyses
6. establish minimum sample-size rules
7. evaluate overall and subgroup performance
8. evaluate calibration
9. quantify uncertainty
10. conduct threshold sensitivity
11. test relevant distribution shifts
12. complete privacy and accessibility review
13. document human oversight, appeal, monitoring, and rollback
14. maintain a risk register
15. pre-specify what blocks progression
16. repeat evaluation after material model or data changes

## Threats to validity

Major threats include:

- historical labels encoding inequity
- subgroup sample sizes being too small
- fairness metrics representing different normative goals
- intersectional analysis increasing privacy risk
- ECE changing with bin choices
- bootstrap assumptions being violated
- threshold tuning on the evaluation set
- shift scenarios being unrealistic
- governance evidence becoming ceremonial
- open risks being accepted without affected-person input
- high technical performance masking pedagogical harm
- passing a checklist being misrepresented as ethical certification

The output is evidence for human review, not a substitute for accountable judgment.
