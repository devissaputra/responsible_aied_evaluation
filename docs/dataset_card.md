# Dataset Card — UCI 697

## Source
**Predict Students' Dropout and Academic Success**  
UCI Machine Learning Repository, dataset 697  
DOI: https://doi.org/10.24432/C5MC89  
Dataset page: https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success  
License reported by UCI: CC BY 4.0.

## Scale
UCI reports 4,424 student instances and 36 predictor features.

## Original task
The source dataset frames the outcome as a three-class classification problem: Dropout, Enrolled, Graduate.

## Bundle transformation
This study converts the outcome to dropout-versus-not-dropout for the narrow purpose of auditing a binary risk probability.

## Temporal boundary
UCI documents both enrollment-time information and first/second-semester academic performance. To construct an enrollment-time scenario, every feature whose name contains `Curricular units 1st sem` or `Curricular units 2nd sem` is excluded.

## Group variables
Gender is reserved for post-hoc audit rather than prediction. Nationality is also excluded from prediction. Group values are preserved as dataset codes in output.

## Population limitation
The data come from one Portuguese higher-education institutional setting across multiple undergraduate programs. Results should not be generalized to other institutions, countries or admission systems without external validation.
