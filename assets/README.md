# Research Bundle Visuals

This directory contains explanatory study-design diagrams.

## Explanatory diagrams

- `architecture.svg` — frozen responsible-AIED empirical architecture;
- `data_flow.svg` — separation of prediction, audit, uncertainty and governance evidence.

These SVG files explain the research protocol and contain no invented empirical scores.

## Generated empirical figures

The real-data workflow writes authoritative figures to `results/figures/`:

- `roc_curve.png`;
- `precision_recall_curve.png`;
- `overall_calibration.png`;
- `gender_calibration.png`;
- `international_calibration.png`;
- `gender_threshold_sensitivity.png`;
- `international_threshold_sensitivity.png`;
- `repeated_split_robustness.png`.

Generated figures come directly from the UCI 697 empirical run.
