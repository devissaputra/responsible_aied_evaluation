# Dataset Card — UCI 697 Responsible AIED Audit

## Source

**Predict Students' Dropout and Academic Success**  
UCI Machine Learning Repository, dataset 697  
DOI: https://doi.org/10.24432/C5MC89  
License: CC BY 4.0

Data descriptor:

Realinho, V., Machado, J., Baptista, L., & Martins, M. V. (2022). *Predicting Student Dropout and Academic Success*. Data, 7(11), 146. https://doi.org/10.3390/data7110146

## Population

The released dataset contains 4,424 student records drawn from a Portuguese higher-education institutional context across multiple undergraduate programs.

## Original endpoint

The source task is three-class classification at the end of the normal course duration:

- Dropout;
- Enrolled;
- Graduate.

This distinction is preserved in provenance and class-count reporting.

## Primary research transformation

The main responsible-evaluation audit creates a binary endpoint:

**Dropout versus no recorded dropout by the source observation endpoint.**

Dropout is coded positive. Enrolled and Graduate are coded negative only for that endpoint definition.

The study does not equate Enrolled with Graduate or call Enrolled a successful outcome.

## Endpoint sensitivity

A separate analysis removes Enrolled observations and compares Dropout against Graduate only.

## Temporal content

The source combines:

- information available at enrollment;
- first-semester performance;
- second-semester performance.

Because the research scenario is enrollment-time prediction, every first- and second-semester curricular-unit field is excluded before fitting.

## Audit-only attributes

The empirical model excludes:

- Gender;
- Nacionality;
- International;
- Educational special needs.

These are used only for audit/group analysis.

Known documented binary meanings are preserved:

- Gender: female / male;
- International: domestic / international;
- Educational special needs: no flag / flag.

Nationality is additionally reduced to Portuguese versus non-Portuguese for a predeclared coarse audit that avoids publishing unstable country-level comparisons from very small cells.

## Proxy limitation

Removing direct demographic attributes does not guarantee that remaining academic, socioeconomic or administrative variables are unrelated to those attributes.

The repository therefore avoids describing the model as demographic-blind or proxy-free.

## Missingness

UCI reports no missing values in the released dataset.

The adapter still validates required audit fields and categorical codes so schema changes or unexpected values fail loudly.

## Reproducibility fingerprint

The generated empirical JSON stores a SHA-256 fingerprint of the retrieved feature matrix and source target in original row/column order.

## Privacy

The dataset is publicly released for research. Student identifiers are not part of this project. No attempt should be made to re-identify individuals.

## External validity

The study does not establish transportability outside the source setting. External institutional and temporal validation would be required before any operational consideration.
