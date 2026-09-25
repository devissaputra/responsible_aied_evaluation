# Dataset Card — UCI 697

## Source

**Predict Students' Dropout and Academic Success**  
UCI Machine Learning Repository, dataset 697  
DOI: https://doi.org/10.24432/C5MC89  
License reported by UCI: CC BY 4.0  
Dataset page: https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success

The empirical runner retrieves the dataset from UCI through `ucimlrepo`. Raw data are not committed.

## Scale and target

UCI reports 4,424 student records and 36 predictors. The source target has three classes: Dropout, Enrolled and Graduate. This bundle defines a binary audit target where Dropout = 1 and Enrolled/Graduate = 0.

## Prediction-time boundary

The scenario is explicitly enrollment-time. Every column containing `Curricular units 1st sem` or `Curricular units 2nd sem` is removed before modeling because those variables occur after enrollment.

`Gender` and `Nacionality` are also excluded from model inputs. Gender is retained only for the held-out group audit.

## Split

A fixed stratified 80/20 holdout uses seed 42. Preprocessing and model fitting occur on the training partition only.

## Limitations

The dataset represents one Portuguese higher-education setting and historical cohorts. The binary target transformation discards the distinction between still-enrolled and graduate students. Group codes are reported as dataset codes rather than reinterpreted beyond the source documentation.
