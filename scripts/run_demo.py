import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from responsible_aied_evaluation.core import demographic_parity_difference, expected_calibration_error

parity=demographic_parity_difference([1,1,0,0],['a','a','b','b'])
ece=expected_calibration_error([.9,.8,.2,.1],[1,1,0,0])
print(f"Demographic parity difference: {parity:.2f}")
print(f"Expected calibration error: {ece:.2f}")
print('The synthetic example intentionally contains a large fairness gap.')
