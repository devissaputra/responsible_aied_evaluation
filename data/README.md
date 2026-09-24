# Data documentation

## Included synthetic data

All files in this folder are synthetic and exist to exercise the responsible-AIED evaluation code.

- `evaluation.csv` contains two scenarios: `baseline` and `shifted`.
- `governance.csv` contains one complete synthetic governance-review record.
- `risks.csv` contains a small educational-AI risk register.
- `decision_thresholds.csv` contains explicit study-specific demo thresholds and rationales.
- `sample.csv` is a compact preview.

No real learner, instructor, institution, protected attribute, or model deployment is represented.

## Evaluation record schema

`evaluation.csv` contains:

- scenario
- case_id
- probability
- binary outcome
- primary group
- intersectional group

The toolkit derives binary predictions from a caller-supplied probability threshold.

## Why probabilities and outcomes are both required

Responsible evaluation should not inspect selection rates alone.

Probabilities support calibration analysis.

Observed outcomes support:

- accuracy
- precision
- recall / true-positive rate
- false-positive rate
- false-negative rate
- Brier score
- calibration analysis

## Group analysis

The synthetic data contain three primary groups and six intersectional group labels.

This is only a software fixture.

A real study must justify:

- which groups are ethically and legally appropriate to evaluate
- whether sample sizes support comparison
- whether intersectional reporting creates privacy risk
- what harm each disparity metric corresponds to

## Governance evidence

`governance.csv` is deliberately more structured than a yes/no deployment checkbox.

A review can require evidence for:

- privacy
- accessibility
- human oversight owner
- appeal path
- rollback authority
- post-deployment monitoring
- accountable decision owner

A boolean marked true without its corresponding evidence field does not pass the implemented governance report.

## Risk register

`risks.csv` uses:

- severity from 1–5
- likelihood from 1–5
- mitigation
- owner
- status

The severity × likelihood score is a simple prioritization aid, not a universal risk model.

## Decision thresholds

`decision_thresholds.csv` is intentionally explicit.

Thresholds are **study-specific demonstration settings**.

They are not universal definitions of fairness, safety, or deployability.

A real evaluation should document who chose each threshold, why, for which population and decision, and what happens when uncertainty overlaps the threshold.

## Shift scenario

The shifted synthetic scenario worsens model behavior for some groups.

It exists to demonstrate that a system that looked acceptable on one sample can become less accurate, less calibrated, or less equitable under changed conditions.

## Before real data are connected

Document:

- intended educational use
- affected population
- decision consequence
- model version
- probability semantics
- label/outcome definition
- group definitions
- consent or lawful basis
- missingness
- subgroup sample sizes
- data collection period
- distribution shift assumptions
- accessibility context
- privacy controls
- retention
- appeal/override process
- monitoring and rollback triggers

## Do not commit

Do not commit identifiable learner records, grades, disability information, protected-attribute data, private LMS exports, free-text submissions, audio/video, or proprietary model outputs unless an approved research environment and governance process explicitly permit them.
