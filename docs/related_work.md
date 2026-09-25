# Related Work and Governance Context

This repository combines empirical educational-model auditing with explicit governance boundaries. It does not claim compliance with any framework.

## Source dataset and educational prediction

Realinho, V., Machado, J., Baptista, L., & Martins, M. V. (2022). *Predicting Student Dropout and Academic Success*. Data, 7(11), 146. https://doi.org/10.3390/data7110146

The data descriptor documents enrollment information, first/second-semester performance variables and the three-state endpoint used in this bundle.

UCI dataset record: https://doi.org/10.24432/C5MC89

## Model documentation

Mitchell et al. introduced model cards as structured documentation for intended use, performance characteristics and limitations.

- Mitchell, M. et al. (2019). Model Cards for Model Reporting. FAT* 2019. https://doi.org/10.1145/3287560.3287596

Gebru et al. proposed datasheets for datasets to make provenance, composition, collection and recommended uses more explicit.

- Gebru, T. et al. (2021). Datasheets for Datasets. Communications of the ACM, 64(12), 86–92. https://doi.org/10.1145/3458723

The repository's dataset and analysis cards draw on that documentation tradition.

## Fairness metrics

Group fairness criteria measure different statistical properties and can be mutually incompatible in realistic settings.

This bundle therefore reports underlying group values plus multiple gaps rather than reducing fairness to one number.

Implemented empirical diagnostics include:

- selection-rate difference;
- TPR/FNR difference;
- FPR difference;
- accuracy difference;
- precision difference;
- equalized-odds-style maximum of TPR/FPR gaps;
- group calibration;
- threshold sensitivity;
- minimum-group-size safeguards.

These are descriptive measurements, not ethical conclusions.

## Calibration

Probability calibration matters because a risk score can be used differently from a hard classification.

The bundle reports:

- Brier score;
- ECE;
- reliability bins;
- calibration intercept;
- calibration slope;
- subgroup calibration.

ECE is retained as one diagnostic while its dependence on binning is explicitly acknowledged.

## NIST AI RMF

NIST AI RMF 1.0 is a voluntary, rights-preserving, use-case-agnostic framework organized around:

- Govern;
- Map;
- Measure;
- Manage.

Reference:

Tabassi, E. (2023). *Artificial Intelligence Risk Management Framework (AI RMF 1.0).* NIST AI 100-1. https://doi.org/10.6028/NIST.AI.100-1

This research bundle is most directly concerned with measurement and with making missing governance evidence visible. It is not a NIST compliance implementation.

## UNESCO AI ethics

UNESCO's 2021 Recommendation on the Ethics of Artificial Intelligence emphasizes human rights, fairness/non-discrimination, transparency, human oversight, data governance and inclusion.

Reference:

UNESCO. *Recommendation on the Ethics of Artificial Intelligence* (2021).

The repository uses those concerns as governance context rather than claiming formal conformance.

## Educational responsible-AI boundary

Prediction quality does not establish beneficial educational intervention.

For this reason, the real-data study deliberately separates:

- model measurement;
- uncertainty;
- subgroup evidence;
- governance evidence gaps;
- intervention claims.

## Current implemented empirical scope

Implemented:

- real UCI educational data;
- frozen enrollment-time boundary;
- protected/audit-only feature separation;
- semantic group labels;
- subgroup and intersectional audits;
- small-group non-evaluability;
- discrimination and PR metrics;
- probability calibration;
- threshold sensitivity;
- conditional holdout bootstrap;
- training-refit bootstrap;
- repeated-split robustness;
- target-definition sensitivity;
- empirical figures;
- governance-evidence gap record;
- educational risk register.

Not implemented:

- causal effect estimation;
- counterfactual fairness;
- privacy attack testing;
- differential privacy;
- production monitoring;
- institution-external validation;
- prospective learner intervention trial;
- legal compliance determination.

Those absences define the boundary of the research claims.
