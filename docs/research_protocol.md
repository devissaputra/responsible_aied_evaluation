# Empirical Research Protocol

## Research question

For an enrollment-time dropout-risk baseline on UCI 697, how stable are predictive quality, calibration and subgroup error/allocation patterns across protected-group definitions, thresholds, train/test splits and target definitions?

## Data source

UCI dataset 697, *Predict Students' Dropout and Academic Success*.

The source endpoint has three states at the end of the normal course duration:

- Dropout;
- Enrolled;
- Graduate.

## Primary endpoint

Primary binary endpoint:

**Dropout by the dataset observation endpoint versus no recorded dropout by that endpoint.**

Encoding:

- Dropout = 1;
- Enrolled/Graduate = 0.

The protocol does not interpret Enrolled as success.

## Target sensitivity

A prespecified secondary analysis removes Enrolled observations and compares:

- Dropout = 1;
- Graduate = 0.

## Prediction time

Enrollment.

All first- and second-semester curricular-unit variables are forbidden predictors.

## Audit-only attributes

The following are excluded from predictive inputs:

- Gender;
- Nacionality;
- International;
- Educational special needs.

They are retained for subgroup evaluation.

Direct removal is a design safeguard, not proof that other predictors contain no proxies.

## Model

L2 logistic regression.

Preprocessing is fit only on the training partition:

- selected continuous variables are standardized;
- remaining coded enrollment-time variables are one-hot encoded;
- unseen categorical values are ignored safely at transformation.

## Primary split

Fixed stratified 80/20 holdout, seed 42.

The test partition is not used for preprocessing or model fitting.

## Overall evaluation

Report:

- prevalence;
- ROC-AUC;
- average precision;
- Brier score;
- log loss;
- ECE;
- calibration slope/intercept;
- balanced accuracy;
- confusion counts/rates.

## Reference threshold

0.50.

This is a descriptive reference threshold only. The study does not optimize a deployment threshold against the test set.

Threshold sensitivity is reported at:

0.30, 0.40, 0.50, 0.60, 0.70.

## Subgroup audits

Primary subgroup dimensions:

- gender;
- international status;
- Portuguese versus non-Portuguese nationality grouping;
- special-needs flag;
- gender × international-status intersection.

Known binary source codes are mapped to documented semantic labels.

## Minimum evidence rule

Minimum group size = 30 holdout cases.

Under-sized groups:

- remain visible in the report;
- are marked non-evaluable for disparity-gap calculation;
- do not contribute to max-min group gaps.

At least two evaluable groups are required for a scored disparity comparison.

## Calibration audit

Overall and group-specific calibration evidence includes:

- Brier score;
- binned calibration tables;
- ECE;
- overall calibration intercept and slope;
- empirical reliability figures.

ECE is treated as a bin-dependent descriptive metric, not a universal calibration certificate.

## Uncertainty

### Conditional holdout bootstrap
1,000 resamples of already-scored holdout records.

For subgroup gaps, resampling is stratified by audit group so original group sample sizes are preserved.

### Training-refit bootstrap
200 stratified resamples of the primary training partition. Preprocessing and logistic regression are refit in every resample; performance and selected group gaps are reevaluated on the fixed untouched primary holdout.

## Repeated-split robustness

The full train/test protocol is repeated across ten prespecified seeds:

11, 23, 42, 73, 101, 131, 173, 211, 257, 307.

The report stores individual results and mean/SD/min/max summaries.

This evaluates split sensitivity, not external transportability.

## Governance and risk

The real-data study does not issue a deployment verdict.

It records:

- missing governance evidence;
- privacy/accessibility/oversight/appeal/rollback/monitoring gaps;
- educational risk register;
- explicit requirement for external and prospective validation before operational use.

## Main threats to validity

- historical labels may encode structural inequities;
- direct protected-feature exclusion does not eliminate proxy information;
- Enrolled is an unresolved third endpoint state;
- subgroup and intersectional cells can be sparse;
- fairness criteria can conflict;
- calibration can vary by population and time;
- one institution limits transportability;
- prediction is not causal evidence;
- no intervention-benefit study is present.
