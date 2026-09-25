# Model Card — Enrollment-Time Dropout Risk Audit

## Purpose
Research evaluation of probability quality and subgroup behavior on UCI 697.

## Model
Logistic regression using enrollment-time predictors only. Gender and nationality are excluded from predictive inputs.

## Outcome
Dropout versus Enrolled/Graduate.

## Intended use
Methodological research, calibration/fairness audit demonstrations, and professor review.

## Not intended for
Automated student labeling, disciplinary decisions, resource denial, mandatory intervention, admissions decisions or claims of individual causation.

## Key limitations
Single institutional context; historical labels; binary target reduction; group codes do not capture all relevant identities; unobserved structural factors; no evidence that acting on the score improves learner outcomes.
