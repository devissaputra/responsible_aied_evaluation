# Dataset Provenance — UCI 697

## Source

**Predict Students' Dropout and Academic Success**  
UCI Machine Learning Repository, dataset 697  
DOI: https://doi.org/10.24432/C5MC89  
License reported by UCI: CC BY 4.0

Data descriptor:

Realinho, V., Machado, J., Baptista, L., & Martins, M. V. (2022). *Predicting Student Dropout and Academic Success*. Data, 7(11), 146. https://doi.org/10.3390/data7110146

The empirical runner retrieves UCI dataset 697 through `ucimlrepo`. Raw learner-level data are not committed to this repository.

## Source scope

UCI reports:

- 4,424 student instances;
- 36 source predictors;
- no missing values in the released dataset;
- information known at enrollment;
- first-semester academic-performance variables;
- second-semester academic-performance variables;
- a three-state endpoint: Dropout, Enrolled, Graduate at the end of the normal course duration.

## Reproducibility fingerprint

Because the runner uses the UCI repository client rather than committing the raw source file, every empirical run computes and records a SHA-256 fingerprint of:

1. the complete normalized UCI feature table;
2. the original source target;
3. original row and column order.

This fingerprint is stored in `results/uci697_audit.json`. A changed upstream table therefore changes the recorded fingerprint.

The fingerprint is a reproducibility guard, not a replacement for the UCI DOI/version record.

## Prediction-time boundary

The frozen scenario is enrollment-time prediction.

Every feature whose name contains either:

- `Curricular units 1st sem`;
- `Curricular units 2nd sem`

is removed before model fitting.

## Audit-only fields

The following source fields are removed from model inputs and retained for subgroup analysis:

- Gender;
- Nacionality;
- International;
- Educational special needs.

UCI documents:

- Gender: 0 = female, 1 = male;
- International: 0 = no, 1 = yes;
- Educational special needs: 0 = no, 1 = yes;
- Nacionality: categorical country codes, including 1 = Portuguese.

The empirical study therefore reports semantic group labels rather than anonymous gender codes.

## Primary target

The source target has three states:

- Dropout;
- Enrolled;
- Graduate.

Primary binary endpoint:

**Dropout by the dataset observation endpoint versus no recorded dropout by that endpoint.**

Thus Enrolled and Graduate are combined only for the primary binary endpoint. Enrolled is not described as academic success.

## Target sensitivity

A prespecified sensitivity analysis excludes Enrolled and compares:

**Dropout versus Graduate.**

This checks whether conclusions depend strongly on combining the unresolved Enrolled state with Graduate.

## Privacy and licensing

The source dataset is public research data. Do not attempt re-identification.

The repository MIT license covers repository code and original materials only. The UCI dataset remains governed by its source license and attribution requirements.

## Generalizability

The dataset represents a historical Portuguese higher-education context across multiple programs at one institutional setting. Results should not be assumed to transport to other institutions, countries, admissions systems or present-day cohorts without external validation.
