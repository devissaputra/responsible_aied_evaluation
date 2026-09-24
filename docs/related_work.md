# Related work and governance context

Responsible AIED Evaluation Toolkit is an original implementation.

It does not reproduce or claim compliance with the frameworks below.

## NIST AI Risk Management Framework

NIST AI RMF 1.0 provides a voluntary, rights-preserving and use-case-agnostic framework for managing AI risks.

It organizes risk-management activity around:

- Govern
- Map
- Measure
- Manage

Reference:

- Tabassi, E. (2023).
- *Artificial Intelligence Risk Management Framework (AI RMF 1.0).*
- NIST AI 100-1.
- https://doi.org/10.6028/NIST.AI.100-1
- https://www.nist.gov/itl/ai-risk-management-framework

This repository reflects the same broad idea that measurement is only one part of responsible AI.

The toolkit additionally requires governance evidence, a risk register, monitoring, and rollback ownership.

NIST AI RMF 1.0 is evolving; this repository should not be described as a NIST compliance implementation.

## UNESCO Recommendation on the Ethics of Artificial Intelligence

UNESCO's Recommendation emphasizes human rights and dignity and includes principles such as:

- fairness and non-discrimination
- transparency and explainability
- human oversight
- data governance
- inclusion

Reference:

- UNESCO. *Recommendation on the Ethics of Artificial Intelligence.*
- Adopted 2021.
- https://www.unesco.org/en/artificial-intelligence/recommendation-ethics

The current repository does not operationalize the full Recommendation.

It uses these principles as governance context for educational AI review.

## UNESCO guidance for generative AI in education and research

UNESCO's education-specific guidance advocates a human-centred approach and highlights privacy, ethical validation, pedagogical design, and institutional preparedness.

Reference:

- Miao, F., & Holmes, W. (2023).
- *Guidance for generative AI in education and research.*
- UNESCO.
- https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research

The present toolkit applies beyond generative AI, but the emphasis on educational purpose, privacy, human agency, and validation is directly relevant.

## Model and dataset documentation

Responsible evaluation also depends on documentation that explains intended use, limitations, data sources, and affected populations.

Relevant traditions include:

- model cards for reporting model purpose, performance, and limitations
- datasheets for documenting dataset provenance, composition, collection, and uses

The repository's system card and data documentation are intentionally aligned with that broader documentation practice.

## Technical fairness and calibration

The toolkit implements transparent binary-classification and probability-evaluation metrics rather than depending on an external fairness library.

Implemented quantitative components include:

- confusion-matrix metrics
- demographic/selection-rate gap
- TPR/FNR gaps
- FPR gap
- equalized-odds-style maximum gap
- accuracy and precision gaps
- calibration bins
- ECE
- maximum calibration error
- Brier score
- group calibration
- bootstrap intervals
- threshold sensitivity
- baseline-versus-shift comparison

These metrics are diagnostics.

They do not by themselves determine what fairness means for a specific educational use.

## Current scope

Implemented:

- overall performance
- subgroup performance
- intersectional grouping
- multiple disparity metrics
- calibration tables
- Brier score
- subgroup calibration
- bootstrap uncertainty
- threshold sensitivity
- scenario-shift comparison
- structured governance evidence
- accessibility review evidence
- appeal path
- rollback owner
- monitoring plan
- educational risk register
- PASS / CONDITIONAL / BLOCK / NOT_EVALUABLE reports

Not implemented:

- legal compliance checking
- differential privacy
- privacy attack testing
- adversarial robustness
- causal fairness
- counterfactual fairness
- automatic accessibility testing
- automated explainability scoring
- environmental impact accounting
- production incident-management integration
- real learner or instructor study

The toolkit is best understood as an auditable evaluation baseline that makes missing evidence visible.
