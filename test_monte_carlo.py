import unittest
import monte_carlo_ttt as mct
import numpy as np


class MonteCarloTest(unittest.TestCase):
    def test_single_node_weight(self):
        n = mct.Node(1, np.zeros((3, 3)))
        n.wins = 1
        n.total = 1

        self.assertEqual(mct.node_weight(n, 1), 1)

    def test_multi_node_weight(self):
        nodes = np.full(5, mct.Node(1, np.zeros((3, 3))))

        weights = mct.node_weight(nodes, 1)
        self.assertTrue(np.all(np.isnan(weights)), msg=weights)


if __name__ == '__main__':
    unittest.main()
