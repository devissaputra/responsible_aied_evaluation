# Calibration, Group Error Patterns and Threshold Sensitivity in an Enrollment-Time Student-Risk Baseline

## Abstract

Responsible evaluation of educational prediction systems requires more than a single accuracy or fairness number. This study audits an enrollment-time logistic-regression baseline on UCI Predict Students' Dropout and Academic Success (dataset 697). Post-enrollment semester-performance variables are excluded by design, gender and nationality are excluded from prediction, and the untouched holdout is evaluated for discrimination, calibration, group error patterns, selection-rate behavior, threshold sensitivity and bootstrap uncertainty. The study is an evaluation audit rather than a deployment or fairness certification.

## Research question

For an enrollment-time dropout-risk baseline, how do overall probability quality and group-level error/allocation metrics vary across gender groups and decision thresholds?

## Data and timing

The source is UCI dataset 697, DOI 10.24432/C5MC89. The source three-class outcome is reframed as Dropout versus Enrolled/Graduate. All first- and second-semester curricular-unit variables are forbidden predictors.

## Model

A logistic-regression pipeline uses train-only preprocessing. Selected continuous features are standardized and coded categorical variables are one-hot encoded. Gender and nationality are not predictive features.

## Evaluation

The fixed stratified 80/20 split uses seed 42. The holdout report includes ROC-AUC, Brier score, ECE, confusion metrics, gender-group selection rate and error metrics, group calibration, threshold sensitivity from 0.30 to 0.70, and bootstrap uncertainty for selected overall/group-gap metrics.

## Results

Numerical results are generated into `results/uci697_audit.json`, `results/summary.md`, and `paper/results.md`. This manuscript intentionally contains no hand-entered fairness verdict.

## Limitations

One historical institution cannot establish transportability. The binary target transformation loses outcome detail. Group metrics depend on sample size, threshold and measurement choices, and parity on one metric can conflict with another. Predictive performance does not demonstrate that an intervention is beneficial.
