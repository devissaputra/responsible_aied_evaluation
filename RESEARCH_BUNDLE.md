# Research Bundle Evidence Contract

## Identity

**Area:** AI in Education  
**Study:** responsible evaluation of an enrollment-time dropout-risk baseline  
**Dataset:** UCI 697 — Predict Students' Dropout and Academic Success

## Frozen design

- unit: one source student record;
- prediction time: enrollment;
- primary endpoint: dropout by source observation endpoint versus no recorded dropout by that endpoint;
- target sensitivity: Dropout versus Graduate, Enrolled excluded;
- primary split: stratified 80/20, seed 42;
- model: logistic regression;
- direct audit-only fields: Gender, Nacionality, International, Educational special needs;
- post-enrollment semester variables: forbidden predictors;
- reference threshold: 0.50, descriptive only;
- minimum subgroup evidence: 30 holdout records.

## Required empirical evidence

A valid generated report records:

1. UCI dataset ID, DOI, license and total sample size;
2. original three-class target counts;
3. normalized dataset SHA-256 fingerprint;
4. exact post-enrollment fields excluded;
5. exact audit-only fields excluded from prediction;
6. prediction feature count;
7. primary endpoint wording and target sensitivity wording;
8. train/test seed and counts;
9. dropout prevalence;
10. ROC-AUC and average precision;
11. Brier score, log loss and ECE;
12. calibration intercept and slope;
13. confusion metrics and balanced accuracy at reference threshold 0.50;
14. semantic gender-group audit;
15. international-status audit;
16. Portuguese/non-Portuguese nationality-group audit;
17. special-needs audit;
18. gender × international intersectional audit;
19. explicit minimum-group-size exclusions;
20. group calibration;
21. threshold sensitivity;
22. conditional holdout bootstrap uncertainty;
23. training-refit bootstrap uncertainty;
24. repeated-split robustness across prespecified seeds;
25. Dropout-versus-Graduate target sensitivity;
26. governance-evidence gaps;
27. educational risk register;
28. exact runtime package versions;
29. generated empirical figures;
30. interpretation/non-deployment boundary.

## Small-group rule

A group below the frozen minimum sample size remains visible with its count and warning but is excluded from disparity-gap calculation.

The study must never silently turn an underpowered group comparison into a numerical fairness conclusion.

## Uncertainty rule

Conditional holdout bootstrap and training-refit bootstrap answer different questions and must remain separately labeled.

Repeated train/test splits are robustness evidence, not a substitute for external validation.

## Governance rule

The real-data study does not execute configurable deployment PASS/BLOCK thresholds.

Governance primitives in the library are retained for inspectable software functionality, but the empirical research output records evidence gaps rather than claiming deployment readiness.

## Authoritative evidence

Machine-readable source:

- `results/uci697_audit.json`

Generated derivatives:

- `results/summary.md`
- `paper/results.md`
- `results/figures/`

## Non-claims

The bundle does not claim:

- a risk score causes dropout;
- removal of direct protected attributes makes the model proxy-free;
- one parity metric defines fairness;
- a threshold of 0.50 is ethically optimal;
- subgroup parity establishes equal learner benefit;
- prediction demonstrates beneficial intervention;
- one institution establishes external validity;
- governance completeness or legal compliance;
- readiness for automated learner intervention.
