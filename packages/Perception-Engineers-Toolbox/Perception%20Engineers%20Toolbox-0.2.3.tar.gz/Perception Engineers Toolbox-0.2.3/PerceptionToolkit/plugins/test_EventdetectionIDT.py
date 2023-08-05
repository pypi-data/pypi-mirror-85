from unittest import TestCase
import yapsy
from yapsy import IPlugin
from PerceptionToolkit.plugins.EventdetectionIDT import EventdetectionIDT
import numpy as np


class TestEventdetectionIDT(TestCase):
    def test_dispersion_salvucci_goldberg(self):
        self.assertTrue(EventdetectionIDT.dispersion_salvucci_goldberg(np.array([10, 0]), np.array([0, 10])) == 20)
        self.assertTrue(EventdetectionIDT.dispersion_salvucci_goldberg(np.array([12.5, 1]), np.array([0, 10])) == 11.5+10)
