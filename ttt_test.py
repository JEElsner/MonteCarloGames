import unittest
import numpy as np

import tic_tac_toe as ttt


class WinTest(unittest.TestCase):
    def test_win_states(self):
        for i in range(3):
            b = np.zeros((3, 3))
            b[i] += 1

            win, winner = ttt.is_win_state(b)
            self.assertTrue(win, msg=i)

            t_win, t_winner = ttt.is_win_state(b.T)
            self.assertTrue(t_win, msg=i)

        b = np.identity(3)
        diag_win, _ = ttt.is_win_state(b)
        self.assertTrue(diag_win)

        b = np.fliplr(b)
        diag2_win, _ = ttt.is_win_state(b)
        self.assertTrue(diag2_win)

    def test_negative_win(self):
        b = np.zeros((3, 3))
        b[0] += -1

        win, winner = ttt.is_win_state(b)
        self.assertTrue(winner, -1)


if __name__ == '__main__':
    unittest.main()
