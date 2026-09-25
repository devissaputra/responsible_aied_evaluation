# Analysis Card — Enrollment-Time Dropout-Risk Responsible Evaluation

## Study role

This is a **research audit of a baseline probability model**, not a deployed student-risk system.

## Model

L2 logistic regression using enrollment-time predictors only.

Preprocessing:

- continuous-variable standardization;
- one-hot encoding for coded categorical variables;
- fitting restricted to the training partition.

## Primary endpoint

Dropout by the dataset observation endpoint versus no recorded dropout by that endpoint.

Enrolled and Graduate are combined only for this binary endpoint. A separate Dropout-versus-Graduate analysis tests sensitivity to that choice.

## Audit-only fields

The model never uses:

- Gender;
- Nacionality;
- International;
- Educational special needs.

These fields remain available for descriptive subgroup evaluation.

## Prediction-time safeguard

All first- and second-semester curricular-unit variables are excluded.

## Evidence reported

Overall:

- prevalence;
- ROC-AUC;
- average precision;
- Brier score;
- log loss;
- ECE;
- calibration slope and intercept;
- balanced accuracy;
- confusion metrics.

Subgroups:

- gender;
- international status;
- nationality grouping;
- special-needs flag;
- gender × international intersection.

Robustness:

- threshold sensitivity;
- conditional holdout bootstrap;
- training-refit bootstrap;
- ten repeated stratified splits;
- alternative target definition.

## Minimum subgroup evidence

Groups with fewer than 30 holdout cases are reported but excluded from disparity-gap calculations.

## Reference threshold

0.50 is used only as a transparent descriptive reference. It is not a deployment recommendation.

## Intended use

- AI in Education research;
- responsible-model-evaluation methods;
- calibration/fairness teaching;
- reproducibility inspection;
- professor and PhD-supervisor review.

## Not intended for

- automated learner labeling;
- grading or admissions;
- sanctions;
- resource denial;
- mandatory intervention;
- disability-related decisions;
- claims of individual causation;
- fairness certification;
- legal compliance determination;
- deployment approval.

## Central limitation

Predictive validity, calibration and subgroup parity do not establish that acting on a risk score improves learner outcomes or avoids harm.
