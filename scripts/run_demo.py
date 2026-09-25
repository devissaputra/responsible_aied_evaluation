import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from responsible_aied_evaluation.core import EvaluationRecord, fairness_report, expected_calibration_error, brier_score

print("Synthetic software fixture only; not an empirical result.")
records=[
    EvaluationRecord("a",.8,1,"g0"),
    EvaluationRecord("b",.3,0,"g0"),
    EvaluationRecord("c",.7,1,"g1"),
    EvaluationRecord("d",.4,0,"g1"),
]
print("ECE:",expected_calibration_error([r.probability for r in records],[r.outcome for r in records],bins=2))
print("Brier:",brier_score([r.probability for r in records],[r.outcome for r in records]))
print("Fairness fixture:",fairness_report(records,min_group_size=1))
