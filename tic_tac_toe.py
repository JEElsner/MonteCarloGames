import numpy as np
import os

import monte_carlo_ttt as mct
from monte_carlo_ttt import Node

os.system('color')

COLOR = {
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'ENDC': '\033[0m',
}

sides = {1: COLOR['YELLOW'] + 'X' + COLOR['ENDC'],
         -1: COLOR['GREEN'] + 'O' + COLOR['ENDC']}


def print_board(board):
    txt = np.arange(board.size).reshape(board.shape).astype(dtype=str)

    for i, c in sides.items():
        txt[board == i] = c

    for v, row in enumerate(txt):
        print(' ' + ' | '.join(row))
        if v != len(txt)-1:
            print('+'.join([('-' * 3) for i in row]))


def is_win_state(board):
    for row in board:
        if np.all(row == row[0]) and row[0] != 0:
            return (True, row[0])

    for col in board.T:
        if np.all(col == col[0]) and col[0] != 0:
            return (True, col[0])

    if np.all(board.diagonal() == board.diagonal()[0]) and board.diagonal()[0] != 0:
        return (True, board.diagonal()[0])

    flipped_diagonal = np.fliplr(board).diagonal()
    if np.all(flipped_diagonal == flipped_diagonal[0]) and flipped_diagonal[0] != 0:
        return (True, flipped_diagonal[0])

    return (False, None)


class Player:
    def __init__(self, side, board):
        self.side = side

    def get_move(self):
        pass

    def notify_move(self, move, side):
        pass


class HumanPlayer(Player):
    def get_move(self):
        return int(input('Place {0} where? '.format(sides[self.side])))

    def notify_move(self, move, side):
        pass


class MonteCarloPlayer(Player):
    def __init__(self, side, board):
        super().__init__(side, board)

        mct.get_winner = lambda state: is_win_state(state)[1]

        self.base_node = Node(side, board)
        self.curr_node = self.base_node

    def get_move(self):
        print('Thinking...')
        # print(len(self.curr_node.children))
        try:
            return self.curr_node.get_move()
        except RuntimeWarning:
            pass

    def notify_move(self, move, side):
        self.curr_node = self.curr_node.next_state(move, side)


def main():
    board = np.zeros((3, 3))

    players = [HumanPlayer(1, board), MonteCarloPlayer(-1, board)][::-1]

    end = False
    winner = None
    while not end:
        for player in players:
            print_board(board)

            location = player.get_move()
            board.flat[location] = player.side

            for watcher in players:
                watcher.notify_move(location, player.side)

            end, winner = is_win_state(board)
            end |= (np.count_nonzero(board) == 9)
            if end:
                break

    print_board(board)

    if winner is not None:
        print(sides[winner], 'wins!')
    else:
        print('The game is a draw!')


if __name__ == '__main__':
    main()
