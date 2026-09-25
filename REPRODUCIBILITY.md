# Reproducibility Protocol

## Install and test

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

## Full empirical run

```bash
python scripts/run_uci_study.py
```

The runner retrieves UCI dataset 697, applies the frozen enrollment-time feature boundary, fits the logistic baseline and writes generated audit evidence.

## Generated evidence

- `results/uci697_audit.json`
- `results/summary.md`
- `paper/results.md`

The JSON contains overall discrimination and calibration, group confusion/error metrics, group calibration, threshold sensitivity and bootstrap uncertainty for selected audit metrics.

## Interpretation

Numerical values are generated from code. Do not copy a favorable metric into the methods documents by hand or treat a rerun as evidence of fairness certification.
