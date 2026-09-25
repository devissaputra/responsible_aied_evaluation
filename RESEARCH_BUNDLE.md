# Research Bundle Evidence Contract

## Identity
**Area:** AI in Education  
**Study:** responsible evaluation of an enrollment-time dropout-risk model  
**Dataset:** UCI 697 — Predict Students' Dropout and Academic Success

## Required empirical evidence
A valid report must state:
1. dataset ID, DOI and sample size;
2. target transformation;
3. all post-enrollment columns excluded by the timing rule;
4. protected variables excluded from prediction;
5. train/test seed and counts;
6. probability model;
7. overall performance and calibration;
8. group-level confusion metrics;
9. disparity metrics with underlying group values;
10. group calibration;
11. threshold sensitivity;
12. limitations and educational harms.

## Non-claims
No output is an ethical certification, legal-compliance determination, learner-benefit estimate, or instruction to intervene.

## Professor review path
`README.md` → `docs/dataset_card.md` → `docs/research_protocol.md` → `scripts/run_uci_study.py` → `src/responsible_aied_evaluation/core.py` → `tests/` → generated empirical JSON.
