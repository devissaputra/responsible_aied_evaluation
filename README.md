# Responsible AIED Evaluation Toolkit

> Multidimensional evaluation for AI in education: performance, calibration, subgroup fairness, uncertainty, threshold sensitivity, scenario shift, educational risk, and governance evidence.

[![CI](https://github.com/devissaputra/responsible_aied_evaluation/actions/workflows/ci.yml/badge.svg)](https://github.com/devissaputra/responsible_aied_evaluation/actions/workflows/ci.yml)

![Responsible AIED Evaluation Toolkit architecture](assets/architecture.svg)

**Area:** Responsible AI in Education · Model Evaluation · AI Governance  
**Status:** working research prototype  
**Author:** Devis Wawan Saputra

## Why this project exists

An educational AI system can have good overall accuracy and still:

- miss needed support for one group
- trigger unnecessary intervention for another group
- produce poorly calibrated probabilities
- degrade after a distribution shift
- rely on tiny subgroup samples
- lack accessibility evidence
- have no meaningful appeal path
- have no named person who can stop deployment
- carry unresolved educational harms

This toolkit treats responsible evaluation as an **evidence-to-decision process**, not a single fairness score or ethics checkbox.

## Important boundary

A result such as:

```text
PASS
```

means only:

> the supplied evidence passed the supplied study-specific rules.

It does **not** mean:

- universally fair
- ethically certified
- legally compliant
- safe for every learner
- pedagogically effective
- ready for unrestricted deployment

## Evaluation architecture

![Responsible AIED Evaluation Toolkit data flow](assets/data_flow.svg)

The implemented review path is:

```text
probabilities + outcomes + groups
               ↓
performance + calibration
               ↓
subgroup fairness
               ↓
uncertainty + threshold sensitivity
               ↓
baseline vs shift comparison
               ↓
governance evidence + educational risks
               ↓
PASS / CONDITIONAL / BLOCK / NOT_EVALUABLE
```

Every review state keeps reasons and mitigation requirements visible.

## Structured evaluation records

`EvaluationRecord` contains:

- case ID
- predicted probability
- observed binary outcome
- primary group
- optional intersectional group

Predictions are derived from an explicit probability threshold rather than stored as hidden assumptions.

## Overall performance

`confusion_metrics()` reports:

- accuracy
- precision
- recall / true-positive rate
- specificity / true-negative rate
- false-positive rate
- false-negative rate
- selection rate
- TP / TN / FP / FN counts

Undefined rates remain `None`.

They are not silently converted to zero.

## Fairness evaluation

The original prototype implemented only demographic-parity difference.

The rebuilt toolkit can inspect:

- group selection rates
- selection-rate gap
- TPR gap
- FPR gap
- FNR gap
- accuracy gap
- precision gap
- equalized-odds-style maximum of TPR and FPR gaps

It also returns the underlying group-level performance table.

### No fake fairness result from one group

The original implementation could effectively imply zero disparity when no meaningful group comparison existed.

The current `fairness_report()` returns:

```text
status = not_evaluable
reason = fewer_than_two_groups
```

when fewer than two groups are available.

## Small subgroup warnings

`group_performance()` and `fairness_report()` accept an explicit minimum group size.

Groups below that threshold remain visible and generate warnings.

The toolkit does not silently treat tiny subgroup estimates as reliable.

## Intersectional analysis

The same fairness functions can evaluate either:

```text
group
```

or:

```text
intersectional_group
```

Intersectional analysis can reveal hidden disparities, but real studies must also consider re-identification and unstable tiny cells.

## Calibration

The toolkit implements:

- calibration bins
- expected calibration error (ECE)
- maximum calibration error (MCE)
- Brier score
- group-level ECE
- group-level Brier score
- between-group ECE gap
- between-group Brier gap

### Calibration bins are inspectable

`calibration_bins()` returns:

- bin boundaries
- sample count
- mean predicted probability
- observed outcome rate
- absolute calibration gap

This is more informative than returning only one ECE number.

## Bootstrap uncertainty

`bootstrap_interval()` provides a reproducible percentile-bootstrap baseline for selected metrics:

- accuracy
- Brier score
- ECE
- selection-rate gap
- TPR gap
- FPR gap

This is a simple uncertainty baseline.

A real study should justify resampling assumptions, clustering, learner repetition, and confidence level.

## Threshold sensitivity

`threshold_sensitivity()` evaluates multiple probability thresholds.

For each threshold it reports:

- accuracy
- overall selection rate
- selection-rate gap
- TPR gap
- FPR gap
- fairness-evaluation status

This helps prevent one arbitrary threshold from being mistaken for a universal property of the system.

## Scenario shift / robustness baseline

`compare_scenarios()` compares baseline and shifted records on:

- accuracy
- Brier score
- ECE
- selection-rate gap
- TPR gap
- FPR gap

The result includes:

- baseline values
- shifted values
- metric deltas

This is a scenario-shift comparison, not a full robustness certification.

## Structured governance evidence

The original gate used:

```python
bool(privacy_reviewed)
bool(human_oversight)
```

which meant a non-empty string such as:

```python
"privacy review failed"
```

could evaluate as `True`.

That failure mode is removed.

`GovernanceReview` now requires actual booleans plus documented evidence or ownership for:

- privacy review
- accessibility review
- human oversight
- appeal path
- rollback plan
- monitoring plan
- accountable decision owner

A `True` checkbox without its required evidence does not pass `governance_report()`.

## Educational risk register

`RiskItem` records:

- risk ID
- description
- severity from 1–5
- likelihood from 1–5
- mitigation
- owner
- status

The toolkit summarizes open risks and their severity × likelihood score.

That score is only a prioritization aid.

It is not a universal model of educational harm.

## Study-specific decision configuration

`DecisionConfig` contains explicit thresholds for:

- probability decision threshold
- maximum ECE
- maximum Brier score
- maximum selection-rate gap
- maximum TPR gap
- maximum FPR gap
- minimum group size
- maximum tolerated open risk score

The toolkit intentionally provides **no universal responsible-AI threshold defaults**.

The caller must supply them.

## Four review states

`responsible_aied_decision()` returns:

### PASS

Configured quantitative checks pass, required governance evidence is complete, no risk exceeds the configured open-risk tolerance, and there are no remaining warnings.

### CONDITIONAL

No configured blocking condition fails, but warnings remain.

A common example is insufficient subgroup sample size.

### BLOCK

One or more metric limits, governance requirements, or open-risk limits fail.

The report includes:

- blocking reasons
- required mitigations

### NOT_EVALUABLE

Required evidence is structurally insufficient.

For example, a fairness review with fewer than two comparison groups returns `NOT_EVALUABLE` rather than pretending disparity is zero.

## Synthetic evaluation suite

![Responsible AIED Evaluation Toolkit synthetic demo](assets/demo_snapshot.svg)

The repository includes:

- **48 synthetic baseline records**
- **48 synthetic shifted records**
- **3 primary groups**
- **6 intersectional group labels**
- structured synthetic governance evidence
- an educational-AI risk register
- explicit study-specific thresholds with rationales

These records are software fixtures.

They are not learner-study data.

## Demo

The demo loads the repository data and prints:

- overall performance
- ECE and Brier score
- subgroup fairness gaps
- group calibration gaps
- bootstrap uncertainty
- threshold sensitivity
- baseline-vs-shift differences
- governance failures
- highest open risk
- final four-state decision report

Run:

```bash
git clone https://github.com/devissaputra/responsible_aied_evaluation.git
cd responsible_aied_evaluation

python scripts/run_demo.py
python -m unittest discover -s tests -v
```

The current implementation uses only the Python standard library.

## Core API

`EvaluationRecord`  
Validated probability, outcome, and group record.

`confusion_metrics(...)`  
Overall or group-level binary performance metrics.

`calibration_bins(...)`  
Inspectable reliability-table baseline.

`expected_calibration_error(...)`  
ECE.

`maximum_calibration_error(...)`  
MCE.

`brier_score(...)`  
Mean squared probability error.

`group_performance(...)`  
Group-level confusion metrics and sample-size warnings.

`fairness_report(...)`  
Multiple disparity metrics with `not_evaluable` support.

`group_calibration_report(...)`  
Group ECE/Brier analysis.

`bootstrap_interval(...)`  
Reproducible percentile bootstrap baseline.

`threshold_sensitivity(...)`  
Threshold-dependent performance/fairness analysis.

`compare_scenarios(...)`  
Baseline-versus-shift metric comparison.

`GovernanceReview` / `governance_report(...)`  
Structured governance evidence.

`RiskItem` / `risk_register_summary(...)`  
Educational-risk tracking.

`DecisionConfig`  
Caller-defined study-specific thresholds.

`responsible_aied_decision(...)`  
Transparent `PASS / CONDITIONAL / BLOCK / NOT_EVALUABLE` review report.

`deployment_gate(...)`  
Backward-compatible legacy helper. New work should use the structured decision API.

## Responsible-AI context

The project is informed by broad responsible-AI risk-management and human-centred principles rather than treating one metric as sufficient.

Relevant context includes:

- NIST AI Risk Management Framework 1.0
- UNESCO Recommendation on the Ethics of Artificial Intelligence
- UNESCO Guidance for generative AI in education and research

See `docs/related_work.md`.

The repository does not claim formal compliance with those frameworks.

## Evaluation checklist

![Responsible AIED Evaluation Toolkit evaluation checklist](assets/evaluation_dashboard.svg)

A credible review should examine at least:

1. **Performance** — what errors does the model make?
2. **Calibration** — do probabilities mean what they claim?
3. **Fairness** — who receives benefit, missed support, or unnecessary intervention?
4. **Uncertainty and robustness** — how stable are conclusions?
5. **Educational risk** — what learner or instructor harms remain open?
6. **Governance** — are privacy, accessibility, oversight, appeal, rollback, and monitoring real and documented?

## Why multiple fairness metrics exist

A selection-rate gap and an error-rate gap answer different questions.

For example:

- unequal TPR/FNR can correspond to unequal access to beneficial support
- unequal FPR can correspond to unequal unnecessary intervention
- unequal selection rates can reveal allocation differences

A real study should connect the metric to the educational consequence before interpreting it.

## Research grounding

### NIST AI RMF

The NIST AI Risk Management Framework treats responsible AI as ongoing risk management rather than a single metric calculation.

The toolkit mirrors that broad structure by combining measurement with governance, risk, monitoring, and mitigation evidence.

### UNESCO AI ethics

UNESCO's Recommendation emphasizes principles including fairness, transparency, inclusion, data governance, and human oversight.

The toolkit does not claim to operationalize the full Recommendation.

### Education-specific AI guidance

UNESCO's guidance for generative AI in education and research emphasizes a human-centred approach, privacy protection, ethical validation, and pedagogical design.

The present toolkit applies beyond generative AI, but those education-specific concerns inform the risk and governance design.

## Responsible-use boundary

Do not treat:

- demographic parity as universal fairness
- one good ECE value as proof of safe probabilities
- a small subgroup estimate as stable evidence
- a PASS state as legal or ethical certification
- governance checkboxes as meaningful without evidence and owners
- model accuracy as proof of educational benefit
- a risk score as a substitute for affected-person judgment

## What the system intentionally does not do

The current repository does not implement:

- legal compliance checking
- differential privacy
- privacy attack simulation
- adversarial attack testing
- causal fairness
- counterfactual fairness
- automated accessibility testing
- automated explainability scoring
- environmental-impact accounting
- production incident-management integration
- real learner outcome validation

Those remain separate research or governance tasks.

## Repository map

```text
.
├── .github/workflows/ci.yml
├── assets/
│   ├── README.md
│   ├── architecture.svg
│   ├── data_flow.svg
│   ├── demo_snapshot.svg
│   └── evaluation_dashboard.svg
├── data/
│   ├── README.md
│   ├── decision_thresholds.csv
│   ├── evaluation.csv
│   ├── governance.csv
│   ├── risks.csv
│   └── sample.csv
├── docs/
│   ├── ethics_and_risks.md
│   ├── related_work.md
│   └── research_protocol.md
├── reports/model_card.md
├── scripts/run_demo.py
├── src/responsible_aied_evaluation/
│   ├── __init__.py
│   └── core.py
├── tests/test_core.py
├── .gitignore
├── CITATION.cff
├── LICENSE
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Research path

A stronger empirical version would:

1. define one concrete educational use case and affected population
2. validate outcome labels and decision consequences
3. pre-specify fairness metrics based on educational harms
4. account for repeated learners/classes/institutions in uncertainty analysis
5. test temporal, institutional, accessibility, language, and curricular shifts
6. include affected learners and instructors in risk review
7. evaluate privacy and security technically where relevant
8. validate accessibility with assistive technologies
9. link monitoring thresholds to incident-response procedures
10. repeat the review after material model, threshold, data, or policy changes
11. evaluate actual learner benefit and harm
12. only then make bounded claims about real-world readiness

## Citation and license

`CITATION.cff` contains the software citation.

Code and original SVG visuals use the MIT License. External frameworks, datasets, standards, and educational resources retain their own terms and licenses.
