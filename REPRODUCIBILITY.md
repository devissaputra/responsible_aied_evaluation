# Reproducibility Protocol

## Development environment

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python -m unittest discover -s tests -v
    python scripts/run_uci_study.py

## Professor-facing pinned environment

Use Python 3.11 with:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements-repro.txt
    python -m unittest discover -s tests -v
    python scripts/run_uci_study.py

The empirical GitHub Actions workflow uses the pinned environment and runs the complete test suite before the real-data study.

## Data reproducibility

The runner retrieves UCI dataset 697 using `ucimlrepo`.

Every successful run records:

- UCI dataset ID;
- DOI;
- license;
- original target counts;
- normalized dataset SHA-256 fingerprint;
- exact runtime package versions.

The fingerprint is calculated over the retrieved feature table plus original target in source row/column order.

## Frozen empirical protocol

The primary run fixes:

- enrollment-time feature boundary;
- direct audit-only fields;
- target definition;
- logistic baseline;
- stratified 80/20 split;
- seed 42;
- reference threshold 0.50;
- minimum subgroup size 30.

Robustness analyses additionally use a fixed list of repeated-split seeds.

## Uncertainty

Two bootstrap procedures are intentionally separated:

### Conditional holdout bootstrap
Resamples already-scored holdout cases. It reflects test-sample variability conditional on one fitted model.

### Training-refit bootstrap
Resamples the original training partition within outcome class, refits preprocessing and logistic regression, and evaluates each refit on the unchanged primary holdout. It reflects model/training-sample instability conditional on the fixed holdout.

Neither procedure replaces external validation.

## Generated evidence

- results/uci697_audit.json;
- results/summary.md;
- paper/results.md;
- results/figures/.

## Workflow publishing

The empirical workflow cancels stale runs when a newer research commit arrives.

Before publishing generated evidence it resets to current `origin/main`, regenerates the study and retries safely if another commit wins the push race. This prevents obsolete generated results from being committed after newer code.

## Interpretation

Reproducing a number verifies computation under the frozen protocol. It does not establish fairness, causal validity, transportability, legal compliance or beneficial educational intervention.
