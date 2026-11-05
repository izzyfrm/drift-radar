import unittest
from drift_radar import compare

class DriftTests(unittest.TestCase):
    def test_identical_distribution(self):
        self.assertAlmostEqual(compare(range(100), range(100))["psi"], 0)

    def test_shift_detected(self):
        self.assertGreater(compare(range(100), range(1000, 1100))["psi"], .2)

    def test_constant_reference(self):
        self.assertGreater(compare([1]*100, [2]*100)["psi"], .2)

    def test_invalid_samples(self):
        for values in [[], [float("nan")], [float("inf")]]:
            with self.assertRaises(ValueError):
                compare([1], values)
