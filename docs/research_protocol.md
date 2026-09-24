# Research protocol

## Project

Responsible AIED Evaluation Toolkit

## Questions

1. Where can an AIED system cause uneven performance or pedagogical harm?
2. Are confidence scores calibrated enough for high-stakes use?
3. What evidence is needed before deployment to learners or instructors?

## Baseline methods

- demographic parity difference
- expected calibration error
- explicit metric thresholds
- privacy review flag
- human oversight gate

## Evidence to collect

Start from the current transparent baseline and record every transformation needed to produce fairness and calibration metrics plus a boolean governance gate. Keep a clear boundary between synthetic demonstration data and any future empirical dataset.

## Validation

Evaluate metrics on a representative holdout set and document why each threshold is appropriate for the decision. Pair quantitative checks with privacy, accessibility, human factors, and domain review.

## What counts as a useful result

The next version should add task specific harm analysis, threshold justification, uncertainty, and multiple fairness definitions. Every metric should be connected to a concrete decision and affected population.

## Threats to validity

Metric choice can hide harms, small subgroups create unstable estimates, historical labels can encode inequity, and governance checkboxes can become ceremonial if no one has authority to act.
