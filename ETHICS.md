# Ethics and Governance Boundary

This repository evaluates an educational prediction model as a research object. It does not recommend deployment.

## Why dropout prediction is high-impact

A student-risk score can influence:

- who receives attention;
- who is monitored;
- how educators interpret learner behavior;
- allocation of support;
- escalation decisions;
- learner autonomy and trust.

False positives can stigmatize learners or trigger unnecessary intervention. False negatives can withhold support. Even accurate predictions can cause harm if the intervention is poorly designed.

## Protected and sensitive information

Gender, nationality, international status and special-needs status are excluded from prediction in the empirical study and retained for subgroup auditing.

Their exclusion does not prove that other variables contain no proxy information.

Special-needs status is treated as particularly sensitive. Under-sized groups are not forced into numerical disparity comparisons.

## Historical-label risk

The outcome reflects historical institutional processes and learner circumstances. It can encode structural inequities, support availability, administrative practices and contextual factors that are not causal properties of the learner.

## Target-definition risk

The source has three endpoint states: Dropout, Enrolled and Graduate.

The primary binary endpoint combines Enrolled and Graduate only as “no recorded dropout by the dataset endpoint.” A separate Dropout-versus-Graduate sensitivity analysis is required.

## Fairness metrics

Selection-rate, TPR, FPR, FNR, precision, accuracy and calibration gaps measure different properties and can conflict.

No single metric is treated as a moral or legal definition of fairness.

## Thresholds

The reference threshold 0.50 exists for transparent comparison only.

A real intervention threshold would require:

- explicit educational objective;
- quantified false-positive/false-negative harms;
- stakeholder participation;
- resource constraints;
- accessibility review;
- prospective intervention evaluation.

## Privacy

The source dataset is public research data, but public availability does not justify re-identification, surveillance expansion or collection of additional sensitive information merely to improve prediction.

## Governance evidence

The empirical study intentionally records deployment-governance evidence as incomplete.

It does not fabricate:

- privacy-impact assessment;
- accessibility assessment;
- human-oversight owner;
- appeal procedure;
- rollback owner;
- production monitoring;
- external validation;
- prospective learner-benefit evidence.

## No automated deployment verdict

The repository's reusable library contains configurable governance-review primitives for software testing and methodological demonstration.

The real-data study does **not** run a PASS/BLOCK deployment gate based on arbitrary fairness cutoffs.

## Excluded uses

Do not use this research bundle alone for:

- admissions;
- grading;
- discipline;
- scholarship decisions;
- disability determination;
- student ranking;
- compulsory intervention;
- automated case escalation;
- employment decisions;
- legal-compliance certification.

## Before operational use

At minimum require:

1. institution-specific data review;
2. external and temporal validation;
3. prospective evidence that the proposed intervention benefits learners;
4. privacy and accessibility review;
5. human oversight with authority to override;
6. meaningful appeal/contestability;
7. monitoring and incident response;
8. rollback authority;
9. subgroup evidence adequate for the affected population;
10. accountable institutional decision ownership.
