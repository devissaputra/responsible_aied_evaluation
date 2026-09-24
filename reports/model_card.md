# Analytic system card

## System

Responsible AIED Evaluation Toolkit

## Purpose

Evaluation utilities for demographic parity, calibration error, and deployment gating with privacy and human oversight checks.

## Current maturity

Working research prototype. The bundled example checks the software path with synthetic inputs. It does not establish validity for real learners, instructors, courses, or workplaces.

## Inputs

See `../data/README.md` for the current synthetic schema and the documentation expected before real data are connected.

## Outputs

The current code produces fairness and calibration metrics plus a boolean governance gate. These outputs are research signals and should be interpreted with the educational context that produced them.

## Evidence needed before real use

Evaluate metrics on a representative holdout set and document why each threshold is appropriate for the decision. Pair quantitative checks with privacy, accessibility, human factors, and domain review.

## Main limitation

No fairness metric is a universal safety test. The current gate is illustrative and cannot replace legal, ethical, privacy, accessibility, or pedagogical review.

## Human oversight

A person must review any output before it can affect a learner, instructor, applicant, or employee.
