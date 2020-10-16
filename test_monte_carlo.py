import unittest

import monte_carlo as mct
import tic_tac_toe as ttt

import numpy as np

from datetime import timedelta


class MonteCarloTest(unittest.TestCase):
    def test_single_node_weight(self):
        n = mct.Node(ttt.TicTacToe())
        n.wins = 1
        n.total = 1

        self.assertEqual(n.weight(1), 1)

    def test_multi_node_weight(self):
        nodes = np.array([mct.Node(ttt.TicTacToe())] * 5)

        weights = mct.Node.v_weight(nodes, 1)
        self.assertTrue(np.all(np.isnan(weights)), msg=weights)

    def test_correct_tic_tac_toe_opening(self):
        game = ttt.TicTacToe()
        node = mct.Node(game)

        dt = mct.decision_time
        mct.decision_time = timedelta(seconds=5)

        move = node.get_move()

        self.assertEqual(
            move, 4, 'Ideal first move of Tic-Tac-Toe is right in the center')

        mct.decision_time = dt


if __name__ == '__main__':
    unittest.main()
