# Empirical Research Protocol

## Question
How do overall performance, calibration and group error/allocation metrics behave for an enrollment-time dropout-risk baseline on UCI 697?

## Prediction time
Enrollment. Semester-performance columns are forbidden predictors.

## Outcome
Dropout = 1; Enrolled or Graduate = 0.

## Model
Logistic regression. Coded categorical variables are one-hot encoded. Selected continuous variables are standardized. Gender and nationality are excluded from predictive inputs.

## Split
Fixed stratified 80/20 holdout with seed 42.

## Evaluation
- confusion metrics;
- Brier score;
- ECE;
- gender-group performance;
- gender-group calibration;
- selection-rate, TPR, FPR, FNR, accuracy, precision and equalized-odds-style gaps;
- threshold sensitivity at 0.30, 0.40, 0.50, 0.60 and 0.70.

## Interpretation
Metrics correspond to different educational harms and normative goals. They can conflict. A smaller gap on one measure can coincide with a larger gap on another.

## Threats
Historical labels may reflect structural inequities. Codes may hide category semantics. One institution limits external validity. Binary target reduction loses the distinction between enrolled and graduate students. Prediction does not demonstrate beneficial intervention.
