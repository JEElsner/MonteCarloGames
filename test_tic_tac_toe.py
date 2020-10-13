import unittest
import numpy as np

import tic_tac_toe as ttt


class TTTTest(unittest.TestCase):
    def test_initialization(self):
        state = ttt.TicTacToe()

        expected_state = np.arange(9).reshape((3, 3)).astype(dtype=str)
        self.assertTrue(np.all(state.get_state() == expected_state),
                        'Initialization and State')

    def test_bad_init_state(self):
        def construct(): return ttt.TicTacToe(board=np.zeros((3, 2)))

        self.assertRaises(ValueError, construct)

    def test_bad_init_player(self):
        def construct(): return ttt.TicTacToe(turn='asdf')

        self.assertRaises(ValueError, construct)

    def test_get_curr_player(self):
        self.assertEqual(ttt.TicTacToe().get_current_turn(), 'X')

    def test_get_moves(self):
        state = ttt.TicTacToe()
        expected_moves = np.arange(9)

        self.assertTrue(np.all(state.get_possible_moves('X') ==
                               expected_moves), 'Empty board move possibilities')

        state.board.flat[8] = 'O'
        self.assertTrue(np.all(state.get_possible_moves('X') ==
                               expected_moves[:-1]), 'Modified board move possibilites')

    def test_move(self):
        state1 = ttt.TicTacToe()

        state2 = state1.move('X', 0)

        expected_state = np.arange(9).reshape(3, 3).astype(dtype=str)
        expected_state.flat[0] = 'X'

        self.assertTrue(np.all(state2.get_state() ==
                               expected_state), 'State after move')
        self.assertNotEqual(state2, state1, 'Move copy')
        self.assertFalse(np.all(state2.board == state1.board),
                         'Move copy board')
        self.assertFalse(np.all(state1.board == expected_state),
                         'Move immutability')

    def test_wrong_turn(self):
        game = ttt.TicTacToe()

        def move_boi(): game.move('O', 0)

        self.assertRaises(ValueError, move_boi)

    def test_win_states(self):
        self.assertIsNone(ttt.TicTacToe().get_winner(), 'No winner')

        for player in ['X', 'O']:
            for i in range(3):
                b = np.arange(9).reshape(3, 3).astype(dtype=str)
                b[i] = player

                game = ttt.TicTacToe(board=b)
                self.assertEqual(game.get_winner(), player,
                                 'Win: {p} Row: {i}'.format(p=player, i=i))

                game = ttt.TicTacToe(board=b.T)
                self.assertEqual(game.get_winner(), player,
                                 'Win: {p} Col: {i}'.format(p=player, i=i))

            b = np.arange(9).reshape(3, 3).astype(dtype=str)
            b[np.identity(3, dtype=bool)] = player
            game = ttt.TicTacToe(board=b)
            self.assertEqual(game.get_winner(), player,
                             'Win: {0} NW-SE Diag'.format(player))

            b = np.fliplr(b)
            self.assertEqual(game.get_winner(), player,
                             'Win: {0} NE-SW Diag'.format(player))


if __name__ == '__main__':
    unittest.main()
