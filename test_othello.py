import othello
import unittest

import numpy as np


def gen_board(light, dark, turn=None) -> othello.Othello:
    b = np.full((8, 8), othello.EMPTY, dtype=str, order='F')

    for coord in light:
        b[coord] = othello.LIGHT

    for coord in dark:
        b[coord] = othello.DARK

    return othello.Othello(b, turn)


class TestOthello(unittest.TestCase):
    def test_no_moves(self):
        state = gen_board([(4, 4)], [], turn=othello.LIGHT)

        self.assertEqual(len(state.get_possible_moves(othello.LIGHT)), 0)

    def test_all_directions_move(self):
        state = gen_board([(4, 4)], [(4, 3), (4, 5), (5, 4), (
                          3, 4), (5, 5), (3, 3), (5, 3), (3, 5)], turn=othello.LIGHT)

        moves = state.get_possible_moves(othello.LIGHT)
        # print(moves)
        self.assertEqual(len(moves), 8)

    def test_diagonal_move(self):
        state = gen_board([(4, 4)], [(5, 4)], turn=othello.LIGHT)

        moves = state.get_possible_moves(othello.LIGHT)

        self.assertEqual(len(moves), 1)
        self.assertEqual(moves[0], (6, 4))


if __name__ == '__main__':
    unittest.main()
