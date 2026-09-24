# Ethics, safety, and misuse risks

## Intended use

Responsible AIED Evaluation Toolkit is a research prototype for structured review of educational AI systems.

It should support accountable human evaluation.

It must not be presented as an automatic ethics certificate, legal opinion, or universal deployment approval mechanism.

## Human rights and educational purpose

Educational AI can affect access to support, attention, opportunities, evaluation, and learner autonomy.

Responsible review should therefore consider:

- fairness and non-discrimination
- privacy and data governance
- transparency
- human oversight
- accessibility
- learner agency
- pedagogical benefit and harm
- contestability
- ongoing monitoring

These concerns align broadly with international responsible-AI guidance, but this repository does not claim formal compliance with any external framework.

## Fairness metrics are not moral verdicts

Different fairness metrics answer different questions.

For example:

- demographic parity concerns selection/allocation rates
- TPR/FNR gaps concern unequal missed benefit
- FPR gaps concern unequal unnecessary intervention
- calibration concerns whether probability meanings differ across groups

These criteria can conflict.

Do not optimize one metric and call the system fair.

Document which harm each metric is intended to detect.

## Small groups and intersectionality

Small-group estimates can be unstable.

Intersectional analysis can reveal hidden harms but can also:

- create tiny cells
- increase re-identification risk
- produce volatile estimates

The current toolkit preserves small-group warnings.

Real studies should define suppression, aggregation, or uncertainty rules before inspecting results.

## Privacy

A responsible review should examine more than whether privacy was "reviewed."

Relevant evidence may include:

- data minimization
- lawful/ethical basis
- direct and indirect identifiers
- sensitive attributes
- retention
- access controls
- secondary use
- de-identification
- deletion
- model-output exposure
- incident response

The current `GovernanceReview` requires a documented privacy evidence field rather than accepting a truthy string as approval.

## Accessibility

AI support can appear technically accurate while excluding learners using assistive technology, alternative input methods, different languages, low-bandwidth devices, or non-standard study workflows.

Accessibility review should therefore be documented as evidence, not assumed from general usability testing.

## Human oversight

Human oversight is meaningful only when someone has:

- a defined role
- enough information to review the output
- authority to override or stop the system
- an escalation pathway
- time and resources to act

The toolkit therefore asks for an oversight owner rather than a bare checkbox.

## Appeal and contestability

Affected learners and instructors should have a meaningful route to question or challenge consequential AI-supported decisions.

The current governance model records an appeal path.

A real deployment should define:

- who receives appeals
- expected response time
- evidence available to the reviewer
- correction and remediation procedure
- protection against retaliation or penalty for appealing

## Rollback

A responsible system needs a named owner who can suspend or roll back use when monitoring identifies unacceptable harm.

Do not deploy a system that no one has authority to stop.

## Monitoring

Performance, calibration, subgroup disparities, and educational effects can change after deployment.

Monitoring plans should specify:

- metrics
- frequency
- trigger thresholds
- incident review
- model/data version
- responsible owner
- rollback criteria

## Educational harm

Technically "correct" interventions may still harm learning.

Examples include:

- interrupting productive struggle
- excessive nudging
- learner labeling
- stigmatization
- dependency
- reduced teacher agency
- inequitable allocation of attention
- surveillance replacing pedagogy

Maintain these harms in the risk register rather than hiding them behind accuracy metrics.

## Decision thresholds

No threshold in this repository should be interpreted as a universal ethical boundary.

Thresholds must be justified for the specific:

- use case
- population
- intervention
- harm severity
- evidence quality
- decision owner

Uncertainty should be considered when results are near a threshold.

## Excluded uses

Do not use this prototype alone for:

- grading
- admissions
- discipline
- scholarship selection
- employment decisions
- psychological or medical diagnosis
- disability determination
- covert surveillance
- automatic high-stakes deployment approval
- legal compliance certification

## Before real deployment

Require at minimum:

- intended-use statement
- affected-population analysis
- performance and calibration evidence
- subgroup and intersectional review where appropriate
- uncertainty analysis
- threshold sensitivity
- relevant shift/robustness testing
- privacy evidence
- accessibility evidence
- human oversight owner
- appeal path
- rollback authority
- monitoring plan
- risk register
- accountable final decision owner

Passing the toolkit means only that the supplied evidence passed the configured review rules.
