# Responsible AIED Evaluation — UCI 697

This bundle audits an enrollment-time dropout probability model across discrimination, calibration, subgroup error patterns, allocation behavior, target definitions, and split sensitivity. Protected-group fields remain audit-only, semester-performance variables are removed to respect the prediction-time boundary, and the results are framed as measurement evidence rather than a fairness certificate.

The primary holdout reports ROC-AUC 0.8316 and Brier score 0.1447. Gender diagnostics can be calculated, while international, intersectional, and special-needs audits remain unevaluable under the support rules. Repeated splits and bootstrap checks describe uncertainty, but incomplete governance evidence and the historical dataset prevent a deployment or fairness certification.

## Start here

- [Calculations, evidence and verification scope](CALCULATIONS.md)
- [Figure sources and exact numerical paths](docs/figure_spec.json)
- [Working paper](paper/paper.md)
- [Data and provenance](DATA.md)

![Study question, data, design and interpretation](assets/review_overview.svg)

![Defined calculation and source-linked evidence](assets/review_calculations.svg)

**Review scope:** The existing suite requires unavailable dependencies; no full-suite pass is claimed. The complete data/model experiment was not rerun in this review. Stored empirical results were inspected, not independently reproduced from raw data.

## Detailed project documentation

[![CI](https://github.com/devissaputra/responsible_aied_evaluation/actions/workflows/ci.yml/badge.svg)](https://github.com/devissaputra/responsible_aied_evaluation/actions/workflows/ci.yml)
[![Empirical Study](https://github.com/devissaputra/responsible_aied_evaluation/actions/workflows/empirical.yml/badge.svg)](https://github.com/devissaputra/responsible_aied_evaluation/actions/workflows/empirical.yml)

**Research Bundle · AI in Education · responsible model evaluation · calibration · subgroup evidence · robustness · governance boundaries**

This repository audits an **enrollment-time student-dropout probability model** using the UCI *Predict Students' Dropout and Academic Success* dataset (dataset 697). The study is designed as a measurement audit: it asks how predictive quality, calibration and group-level error/allocation behavior vary under a frozen modeling protocol.

It does **not** turn those measurements into a fairness certificate or deployment recommendation.


## Research question

For an enrollment-time dropout-risk baseline, how stable are discrimination, probability calibration and subgroup error/allocation patterns across protected-group definitions, reference thresholds, train/test splits and target definitions?

## Real dataset

UCI dataset 697 contains 4,424 student records. The source outcome has three states at the end of the normal course duration:

- Dropout;
- Enrolled;
- Graduate.

The source combines enrollment-time demographic, academic and socioeconomic information with first- and second-semester performance variables.

Dataset DOI: **10.24432/C5MC89**  
Source data paper: Realinho et al. (2022), *Data*, 7(11), 146, DOI **10.3390/data7110146**.

## Frozen prediction-time boundary

The prediction scenario is **enrollment time**.

The empirical adapter therefore removes every feature containing:

- `Curricular units 1st sem`;
- `Curricular units 2nd sem`.

The following fields are also **audit-only** and never enter the prediction model:

- `Gender`;
- `Nacionality`;
- `International`;
- `Educational special needs`.

This closes the previous direct proxy problem where nationality was excluded but international status remained predictive.

Holding these variables out does **not** prove the remaining feature set is proxy-free.

## Endpoint definition

The primary binary endpoint is:

**Dropout by the dataset observation endpoint versus no recorded dropout by that endpoint.**

Accordingly:

- Dropout = 1;
- Enrolled or Graduate = 0.

This does **not** treat Enrolled as academic success. Because Enrolled remains a distinct unresolved source state, the bundle also runs a prespecified **Dropout-versus-Graduate sensitivity analysis that excludes Enrolled cases**.

## Model

The baseline is deliberately interpretable and modest:

- logistic regression;
- train-only preprocessing;
- standardization of selected continuous variables;
- one-hot encoding of coded categorical variables;
- fixed primary stratified 80/20 split, seed 42.

No protected/audit-only variable is used in model fitting.

## Evaluation

The primary untouched holdout reports:

- dropout prevalence;
- ROC-AUC;
- average precision / PR performance;
- Brier score;
- log loss;
- ECE;
- calibration intercept and slope;
- balanced accuracy and confusion metrics at reference threshold 0.50;
- subgroup selection rate, TPR, FPR, FNR, accuracy and precision;
- subgroup calibration;
- threshold sensitivity.

The threshold of 0.50 is a **descriptive reference threshold**, not an optimized or ethically preferred intervention threshold.

## Subgroup evidence

The empirical study audits:

- female versus male;
- domestic versus international;
- Portuguese versus non-Portuguese nationality grouping;
- special-needs flag versus no recorded special-needs flag;
- gender × international-status intersections.

Known UCI code semantics are used rather than opaque labels. Groups below the frozen minimum evidence threshold are retained in the record but **excluded from disparity-gap calculations**.

## Robustness and uncertainty

The bundle separates several sources of uncertainty instead of presenting one interval as universal:

1. **Conditional holdout bootstrap** — resamples already-scored holdout cases; useful for test-sample uncertainty conditional on the fitted model.
2. **Training-refit bootstrap** — resamples the training partition by outcome class, refits preprocessing and model each time, then evaluates the untouched holdout.
3. **Repeated stratified splits** — reruns the full train/test protocol over ten prespecified seeds.
4. **Target sensitivity** — repeats the study for Dropout versus Graduate only.

## Governance boundary

The underlying library contains governance and risk-review primitives, but the empirical study deliberately produces **no deployment PASS/BLOCK verdict**.

Instead it records which deployment evidence is missing: privacy review, accessibility review, human-oversight ownership, appeal, rollback, monitoring, external validation and prospective evidence of learner benefit.

## Reproduce

Development environment:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python -m unittest discover -s tests -v
    python scripts/run_uci_study.py

Professor-facing pinned environment:

    pip install -r requirements-repro.txt
    python -m unittest discover -s tests -v
    python scripts/run_uci_study.py

## Evidence map

| Evidence | Location |
|---|---|
| Dataset provenance and endpoint semantics | DATA.md |
| Frozen empirical protocol | docs/research_protocol.md |
| Dataset card | docs/dataset_card.md |
| Responsible-AI context | docs/related_work.md |
| Ethics and misuse boundary | ETHICS.md |
| Executable empirical adapter | scripts/run_uci_study.py |
| Evaluation engine | src/responsible_aied_evaluation/core.py |
| Core + adapter tests | tests/ |
| Machine-readable empirical evidence | results/uci697_audit.json |
| Generated summary | results/summary.md |
| Empirical figures | results/figures/ |
| Manuscript | paper/paper.md |
| Analysis card | reports/model_card.md |
| Evidence contract | RESEARCH_BUNDLE.md |

## Interpretation boundary

A predictive association is not a causal effect. A small group gap is not proof of fairness. A well-calibrated score is not proof that an intervention based on it benefits learners.

This repository is intended for transparent responsible-AIED research and professor review, not learner ranking or automated educational decision-making.
