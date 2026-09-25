# Responsible AIED Evaluation — Research Bundle

[![CI](https://github.com/devissaputra/responsible_aied_evaluation/actions/workflows/ci.yml/badge.svg)](https://github.com/devissaputra/responsible_aied_evaluation/actions/workflows/ci.yml)

**Research Bundle · AI in Education · calibration, subgroup error analysis and governance boundaries**

This repository now pairs its responsible-AI evaluation engine with a real empirical study using **UCI Predict Students' Dropout and Academic Success (dataset 697)**. The previous synthetic evaluation suite has been removed from the research data directory; tiny fixtures remain only inside tests and the smoke demo.

## Research question

> For an enrollment-time student-dropout risk model, how do overall discrimination, probability calibration and error/selection disparities vary across the dataset's gender groups and across decision thresholds?

The study is an **evaluation audit**, not a deployment proposal. It deliberately avoids translating one metric into a claim that a system is fair, ethical or safe.

## Real dataset

UCI dataset 697 contains 4,424 student records and 36 predictors from a Portuguese higher-education institution, with a three-class outcome: `Dropout`, `Enrolled`, or `Graduate`.

UCI states that the data include:
- information known at enrollment;
- first-semester performance;
- second-semester performance.

For an enrollment-time research scenario, this bundle **excludes all first- and second-semester curricular-unit variables** before training.

Dataset DOI: 10.24432/C5MC89  
License reported by UCI: CC BY 4.0.

## Frozen empirical design

### Outcome
Binary audit target:
- 1 = `Dropout`
- 0 = `Enrolled` or `Graduate`

This binary reframing is a study choice and is documented as such.

### Prediction-time boundary
All columns containing `Curricular units 1st sem` or `Curricular units 2nd sem` are excluded to avoid using post-enrollment academic performance in an enrollment-time model.

### Protected/group variables
`Gender` is held out of the predictive feature set and used as an audit group. `Nacionality` is also excluded from prediction. The script reports group codes exactly as represented by the dataset rather than inventing semantic labels.

### Model
Logistic regression with:
- one-hot encoding for coded categorical variables;
- scaling for selected continuous variables;
- train-only fitting;
- fixed stratified 80/20 holdout, seed 42.

### Evaluation
The untouched holdout is used for:
- accuracy/precision/recall/specificity and confusion counts;
- Brier score;
- ECE;
- group selection-rate, TPR, FPR, FNR, accuracy and precision gaps;
- group calibration;
- threshold sensitivity.

No universal fairness thresholds are imposed.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_uci_study.py
```

The empirical report is written to `results/uci697_audit.json`.

## Why this qualifies as a Research Bundle

- real educational data with DOI and license;
- a frozen prediction-time boundary;
- protected-feature separation;
- explicit model and split;
- calibration plus performance;
- multiple subgroup metrics rather than one “fairness score”;
- threshold sensitivity;
- non-evaluable/small-group safeguards in the core toolkit;
- ethics/governance boundaries;
- CI/tests and paper-ready protocol.

See [RESEARCH_BUNDLE.md](RESEARCH_BUNDLE.md).

## Critical boundary

A risk score can create harm through false positives, false negatives, stigmatization, surveillance, differential intervention and self-fulfilling feedback loops. This repository does not recommend automated student intervention and does not claim that demographic parity, equalized odds, calibration or any other single metric defines fairness.
