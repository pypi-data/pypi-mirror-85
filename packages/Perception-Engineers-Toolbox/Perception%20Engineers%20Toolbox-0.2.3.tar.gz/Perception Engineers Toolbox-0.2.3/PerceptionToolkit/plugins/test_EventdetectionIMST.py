from unittest import TestCase
from PerceptionToolkit.plugins.EventdetectionIMST import EventdetectionIMST
import numpy as np


class TestEventdetectionIMST(TestCase):
    def test_primMST(self):
        g = EventdetectionIMST.Graph(4)
        g.graph = [[0, 0, 1, 2], [0, 0, 0, 2], [1, 0, 0, 3], [2, 2, 3, 0]]
        self.assertTrue(EventdetectionIMST.Graph.primMST(g, 4) == [[3, 1, 2], [0, 2, 1], [0, 3, 2]])