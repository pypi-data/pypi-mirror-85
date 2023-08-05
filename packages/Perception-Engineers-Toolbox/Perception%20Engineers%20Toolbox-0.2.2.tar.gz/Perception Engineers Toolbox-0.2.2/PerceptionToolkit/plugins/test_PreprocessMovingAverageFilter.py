from unittest import TestCase
from PerceptionToolkit.plugins.PreprocessMovingAverageFilter import *
import numpy as np


class TestPreprocessMovingAverageFilter(TestCase):

    """
    def test_convolving_mean(self):
        self.run_conv_test(np.ones(4), np.ones(4), 3)
        self.run_conv_test(np.array([1.0, 2, 1, 2]), np.array([1, (1 + 2 + 1) / 3, (2 + 1 + 2) / 3, 2]), 3)
        self.run_conv_test(np.array([1.0, 7, 3, np.nan]), np.array([1, (1.0 + 7 + 3) / 3, 3, np.nan]), 3)

    def run_conv_test(self, data: np.array, result: np.array, n: int) -> None:
        print(PreprocessMovingAverageFilter.convolving_mean(data, n))
        self.assertTrue(np.allclose(PreprocessMovingAverageFilter.convolving_mean(data, n), result, equal_nan=True))
    """
