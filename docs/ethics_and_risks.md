# Ethics, Validity, and Misuse Risks

## Research purpose

The repository asks whether a transparent enrollment-time baseline can be evaluated responsibly across predictive quality, calibration, subgroup behavior, uncertainty and governance evidence.

It does not ask whether the model should be deployed.

## Risk 1 — historical labels

Dropout status is an observed historical endpoint, not a direct measurement of ability, motivation or educational worth.

Institutional processes, finances, work constraints, health, disability, support, discrimination and many other factors can influence the observed outcome.

**Mitigation:** describe the target narrowly, avoid learner-essentialist interpretations and require causal/prospective evidence before intervention claims.

## Risk 2 — endpoint compression

The original dataset contains Dropout, Enrolled and Graduate.

Combining Enrolled and Graduate into one negative class can obscure meaningful differences.

**Mitigation:** name the primary endpoint “no recorded dropout by the source observation endpoint” and run Dropout-versus-Graduate sensitivity analysis.

## Risk 3 — direct/proxy discrimination

Removing Gender, Nacionality, International and Educational special needs prevents direct use of those fields, but remaining predictors can still carry correlated information.

**Mitigation:** never claim the model is proxy-free; audit outcomes by held-out group attributes and treat causal explanations as unresolved.

## Risk 4 — sparse groups

International, special-needs and intersectional populations can be small.

**Mitigation:** predeclare minimum group size 30. Under-sized groups remain visible but do not enter disparity-gap computation.

## Risk 5 — metric conflict

Demographic/selection parity, error-rate parity and calibration can disagree.

**Mitigation:** report multiple metrics with their underlying group values and avoid composite “fairness scores.”

## Risk 6 — threshold misuse

Threshold choice changes both overall errors and subgroup gaps.

**Mitigation:** treat 0.50 as a reference only and publish threshold sensitivity from 0.30 to 0.70.

## Risk 7 — calibration instability

ECE depends on binning, while calibration can shift across populations.

**Mitigation:** report Brier score, calibration bins, ECE, calibration slope/intercept, subgroup calibration and empirical reliability figures.

## Risk 8 — uncertainty understatement

A bootstrap over fixed predictions does not capture model-fitting uncertainty.

**Mitigation:** separate conditional holdout bootstrap from a training-refit bootstrap, and add repeated train/test split robustness.

## Risk 9 — transportability

One historical institutional context does not establish contemporary or cross-institution validity.

**Mitigation:** label repeated splits as internal robustness only and require external/temporal validation.

## Risk 10 — intervention harm

Even a predictive score with strong discrimination can produce harmful or ineffective interventions.

**Mitigation:** no deployment verdict; require prospective evaluation of the intervention itself.

## Governance evidence intentionally absent

The research run does not manufacture evidence for:

- privacy impact;
- accessibility;
- human-oversight ownership;
- appeals;
- rollback;
- monitoring;
- external validation.

Those absences are recorded as evidence gaps.

## Bottom line

The responsible output of this study is not “fair” or “safe.”

The responsible output is a transparent record of what was measured, how stable it was, what was not measured, and what would still be required before a consequential educational decision.
