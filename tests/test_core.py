import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from responsible_aied_evaluation import core


class CoreTests(unittest.TestCase):
    def test_fairness_calibration_and_gate(self):
        gap = core.demographic_parity_difference([1, 1, 0, 0], ["a", "a", "b", "b"])
        self.assertAlmostEqual(gap, 1.0)
        self.assertAlmostEqual(core.expected_calibration_error([0.9, 0.8, 0.2, 0.1], [1, 1, 0, 0]), 0.15)
        self.assertTrue(core.deployment_gate(0.05, 0.05, True, True))

    def test_mismatched_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            core.expected_calibration_error([0.5], [0, 1])


if __name__ == "__main__":
    unittest.main()
