# Responsible Evaluation of an Enrollment-Time Student Dropout-Risk Baseline: Calibration, Subgroup Evidence, Robustness and Governance Boundaries

## Abstract

Educational risk prediction can appear technically convincing while remaining weakly justified for consequential use. This study audits a deliberately simple enrollment-time logistic-regression baseline using UCI dataset 697, *Predict Students' Dropout and Academic Success*. The protocol removes first- and second-semester performance variables to enforce an enrollment-time prediction boundary. Gender, nationality, international status and special-needs status are withheld from prediction and reserved for subgroup evaluation. The primary endpoint is dropout by the source observation endpoint versus no recorded dropout by that endpoint; because the source also contains an Enrolled state, a Dropout-versus-Graduate sensitivity analysis is prespecified. Evaluation covers discrimination, precision-recall performance, probability calibration, subgroup error/allocation patterns, intersectional evidence, threshold sensitivity, conditional holdout bootstrap uncertainty, training-refit bootstrap uncertainty and repeated train/test splits. The empirical study records governance-evidence gaps and educational risks rather than issuing a fairness or deployment verdict.

## 1. Research question

For an enrollment-time dropout-risk baseline, how stable are predictive quality, calibration and subgroup error/allocation patterns across protected-group definitions, reference thresholds, train/test splits and target definitions?

## 2. Dataset

The source is UCI dataset 697, *Predict Students' Dropout and Academic Success*, DOI 10.24432/C5MC89.

The accompanying data descriptor is:

Realinho, V., Machado, J., Baptista, L., & Martins, M. V. (2022). Predicting Student Dropout and Academic Success. *Data, 7*(11), 146. https://doi.org/10.3390/data7110146

The dataset contains 4,424 student records from a Portuguese higher-education institutional context. It combines information known at enrollment with first- and second-semester academic-performance measures.

The source outcome is recorded at the end of the normal course duration and has three states:

- Dropout;
- Enrolled;
- Graduate.

## 3. Prediction-time design

The research scenario is enrollment-time risk estimation.

All source columns containing `Curricular units 1st sem` or `Curricular units 2nd sem` are excluded before fitting. This prevents post-enrollment performance variables from leaking future information into an enrollment-time model.

The following fields are also excluded from prediction and retained for subgroup analysis:

- Gender;
- Nacionality;
- International;
- Educational special needs.

The earlier repository version excluded nationality but still allowed International into the predictor set. The current protocol removes both because international status is directly related to nationality context.

This does not establish that the remaining feature set is proxy-free.

## 4. Outcome definition

### 4.1 Primary endpoint

The primary binary endpoint is:

**Dropout by the dataset observation endpoint versus no recorded dropout by that endpoint.**

Dropout is positive. Enrolled and Graduate are negative only for this endpoint definition.

The wording is intentional: Enrolled is not described as academic success.

### 4.2 Target sensitivity

A secondary prespecified analysis excludes Enrolled cases and compares Dropout against Graduate.

This tests whether model and subgroup conclusions are sensitive to the unresolved Enrolled state.

## 5. Model

The baseline is L2 logistic regression.

Continuous variables in the frozen preprocessing map are standardized. Remaining coded enrollment-time variables are one-hot encoded.

All preprocessing is fit on the training partition only.

The objective is not to maximize predictive performance. A transparent baseline makes the evaluation protocol inspectable and limits the temptation to hide responsible-AI questions behind model complexity.

## 6. Primary split

The primary design uses a stratified 80/20 train/test split with seed 42.

The test partition is untouched during preprocessing and fitting.

The reference probability threshold is 0.50. It is used only to make confusion and subgroup metrics comparable; it is not described as an optimal educational decision threshold.

## 7. Overall evaluation

The holdout report includes:

- dropout prevalence;
- ROC-AUC;
- average precision;
- Brier score;
- log loss;
- expected calibration error;
- calibration intercept;
- calibration slope;
- balanced accuracy;
- confusion counts and rates.

ROC-AUC and average precision are reported together because the positive class is not balanced and ranking quality should not be summarized by ROC-AUC alone.

## 8. Subgroup evaluation

The study audits:

- female versus male;
- domestic versus international;
- Portuguese versus non-Portuguese;
- special-needs flag versus no recorded special-needs flag;
- gender × international-status intersections.

Gender and international codes are mapped to the semantics documented by the source rather than reported as opaque numeric codes.

### 8.1 Minimum evidence

A frozen minimum of 30 holdout observations is required for a group to contribute to disparity-gap calculations.

Small groups remain visible with their sample sizes and warnings. If fewer than two groups are evaluable, no disparity gap is scored.

This rule is particularly important for international, special-needs and intersectional groups.

## 9. Fairness-metric interpretation

The study reports selection-rate, TPR, FPR, FNR, accuracy and precision behavior by group.

These metrics answer different questions and can conflict. The study does not combine them into a single fairness score.

An equalized-odds-style diagnostic is reported as the larger of the TPR and FPR gaps. It remains a statistical diagnostic, not a normative fairness conclusion.

## 10. Calibration

Probability quality is evaluated using:

- Brier score;
- ECE;
- calibration bins/reliability data;
- calibration intercept;
- calibration slope;
- group calibration.

ECE is acknowledged as bin-dependent. It is not used as a stand-alone calibration verdict.

## 11. Threshold sensitivity

Group and overall behavior is recomputed at thresholds:

0.30, 0.40, 0.50, 0.60, 0.70.

This demonstrates that an apparently favorable or unfavorable group gap can change when the operational threshold changes.

The study does not select a threshold by optimizing fairness on the holdout.

## 12. Uncertainty

### 12.1 Conditional holdout bootstrap

The already-scored holdout is resampled 1,000 times.

For group-gap metrics, resampling is stratified by group so the original group sample sizes are preserved.

These intervals describe test-sample variation conditional on the fitted model.

### 12.2 Training-refit bootstrap

The primary training partition is resampled 200 times within outcome class.

For every resample:

1. preprocessing is refit;
2. logistic regression is refit;
3. predictions are regenerated for the unchanged primary holdout;
4. performance and selected subgroup-gap metrics are recomputed.

This captures model/training-sample instability conditional on the fixed test set.

## 13. Repeated-split robustness

The complete train/test protocol is rerun using ten prespecified seeds:

11, 23, 42, 73, 101, 131, 173, 211, 257, 307.

The generated report stores each split and summary mean, standard deviation, minimum and maximum.

Repeated splits are internal robustness evidence, not external validation.

## 14. Governance and educational risk

The reusable library includes governance-evidence and risk-register primitives. The empirical study integrates them without producing a deployment verdict.

The generated evidence explicitly records missing deployment prerequisites, including:

- privacy review;
- accessibility review;
- accountable human oversight;
- appeal process;
- rollback authority;
- production monitoring;
- external validation;
- prospective evidence of intervention benefit.

The accompanying risk register covers historical-label bias, false-positive harm, target compression, sparse subgroup evidence and transportability.

## 15. Results

Numerical results are generated automatically into:

- `results/uci697_audit.json`;
- `results/summary.md`;
- `paper/results.md`;
- `results/figures/`.

This manuscript intentionally avoids hand-entering a favorable model or fairness conclusion.

## 16. Limitations

First, the dataset represents one historical institutional context.

Second, the primary binary endpoint compresses a three-state outcome, although a target sensitivity analysis addresses this explicitly.

Third, removing direct protected attributes does not remove proxy information.

Fourth, subgroup metrics can remain uncertain or non-evaluable when groups are small.

Fifth, calibration and group behavior can shift over time or institutions.

Sixth, predictive association is not causal evidence.

Finally, no evidence in this repository demonstrates that acting on the model improves learner outcomes.

## 17. Ethics and use boundary

The repository should not be used for automated learner labeling, admissions, grading, discipline, resource denial, disability determination or compulsory intervention.

A responsible operational study would require institution-specific validation, stakeholder participation, privacy/accessibility review, prospective intervention evaluation, contestability, human oversight, monitoring and rollback authority.

## References

Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., & Crawford, K. (2021). Datasheets for Datasets. *Communications of the ACM, 64*(12), 86–92. https://doi.org/10.1145/3458723

Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D., & Gebru, T. (2019). Model Cards for Model Reporting. *FAT* 2019*. https://doi.org/10.1145/3287560.3287596

Realinho, V., Machado, J., Baptista, L., & Martins, M. V. (2022). Predicting Student Dropout and Academic Success. *Data, 7*(11), 146. https://doi.org/10.3390/data7110146

Tabassi, E. (2023). *Artificial Intelligence Risk Management Framework (AI RMF 1.0).* NIST AI 100-1. https://doi.org/10.6028/NIST.AI.100-1

UNESCO. (2021). *Recommendation on the Ethics of Artificial Intelligence.*
