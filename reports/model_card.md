# Analytic system card

## System

Responsible AIED Evaluation Toolkit

## Purpose

Multidimensional evaluation of educational AI systems across performance, calibration, subgroup disparities, uncertainty, threshold sensitivity, scenario shift, educational risk, and governance readiness.

## Current maturity

Working research prototype.

All bundled prediction records, groups, governance evidence, risks, thresholds, and shift scenarios are synthetic.

The toolkit demonstrates evaluation structure and software behavior.

It does not establish that a real educational AI system is safe, fair, lawful, ethical, or effective.

## Inputs

### Evaluation records

Each `EvaluationRecord` contains:

- case ID
- predicted probability
- observed binary outcome
- primary group
- optional intersectional group

### Governance evidence

`GovernanceReview` records:

- privacy review
- accessibility review
- human oversight
- appeal path
- rollback plan
- monitoring plan
- accountable decision owner
- evidence/owner text for each required governance area

### Risk register

Each `RiskItem` records:

- risk ID
- description
- severity
- likelihood
- mitigation
- owner
- status

### Decision configuration

`DecisionConfig` contains explicit study-specific thresholds for:

- probability decision threshold
- ECE
- Brier score
- selection-rate gap
- TPR gap
- FPR gap
- minimum group size
- maximum tolerated open risk score

The package does not provide universal default ethical thresholds.

## Quantitative outputs

### Overall performance

- accuracy
- precision
- recall / TPR
- specificity
- FPR
- FNR
- selection rate
- TP/TN/FP/FN counts

### Fairness / subgroup diagnostics

- group-level performance
- selection-rate gap
- TPR gap
- FPR gap
- FNR gap
- accuracy gap
- precision gap
- equalized-odds-style maximum gap
- small-group warnings
- primary or intersectional group analysis

### Calibration

- calibration-bin table
- ECE
- maximum calibration error
- Brier score
- group ECE
- group Brier
- between-group calibration gaps

### Uncertainty and sensitivity

- bootstrap interval baseline
- threshold sensitivity
- baseline-vs-shift metric comparison

## Decision report

The main review function can return:

- `PASS`
- `CONDITIONAL`
- `BLOCK`
- `NOT_EVALUABLE`

It also reports:

- blocking reasons
- warnings
- required mitigations
- fairness evidence
- calibration evidence
- governance failures
- risk summary
- exact decision configuration

## Important interpretation boundary

A PASS result means:

> the supplied evidence passed the supplied study-specific rules.

It does **not** mean:

- universally fair
- ethically certified
- legally compliant
- educationally effective
- safe for every learner
- ready for unrestricted deployment

## Main limitations

The current toolkit:

- assumes binary outcomes
- uses simple group-disparity metrics
- uses a basic percentile bootstrap
- does not model clustered/repeated learner observations
- does not estimate causal effects
- does not test adversarial attacks
- does not perform privacy attacks
- does not automate accessibility testing
- does not validate educational benefit
- depends on caller-defined group choices and thresholds
- cannot resolve normative conflicts among fairness definitions

## Human oversight

A responsible review should name who can:

- interpret the evidence
- challenge the result
- approve progression
- pause deployment
- handle appeals
- own rollback
- monitor post-deployment behavior

The toolkit records these governance elements so that "human oversight" is not reduced to a bare boolean.

## Evidence needed before real use

A real evaluation should provide:

- intended use
- affected population
- decision consequence
- model/data version
- outcome validity
- group definitions
- sample sizes
- uncertainty
- educational harm model
- threshold rationale
- privacy review
- accessibility review
- human oversight
- appeal path
- rollback
- monitoring
- risk register
- accountable final decision owner
