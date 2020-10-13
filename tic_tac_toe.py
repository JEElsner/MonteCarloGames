import numpy as np
import os

from game import GameState
from vectorize_objects import vectorize

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


class TicTacToe(GameState):
    def __init__(self, board=None, turn=None):
        self.players = ['X', 'O']

        if board is None:
            # If starting a new game
            shape = np.array([3, 3])

            self.board = np.arange(np.product(shape)).reshape(
                shape).astype(dtype=str)
        elif np.all(np.array(board.shape) == board.shape[1:]):
            # If continuing a game, and the board is properly configured
            self.board = board
        else:
            raise ValueError('Invalid initializing board size')

        # If we have a custom starting player
        if turn is not None:
            # Make sure the current turn is valid
            if turn in self.players:
                # Loop until we get to the current player's turn
                while self.players[0] != turn:
                    self.players.append(self.players.pop(0))
            else:
                raise ValueError('Invalid initializing player')

        # Vectorize the TicTacToe class
        vectorize(TicTacToe)

    def get_state(self):
        '''
        Returns the state of the game board
        '''
        return self.board

    def get_current_turn(self):
        '''
        Returns the player whose turn it currently is. (Players are 'X' and 'O')
        '''
        return self.players[0]

    def get_possible_moves(self, player):
        '''
        Return the possible moves as a list of integers as the index of each
        square in the Tic-Tac-Toe grid.
        '''
        return np.arange(self.board.size)[np.char.isdigit(self.board.flat)]

    def move(self, player, move):
        '''
        Returns a new TicTacToe object representing the next state of the game
        after this move is made.

        Arguments:

            player      The player who is making this move

            move        The integer representing the index of the square to
                        place the player's piece
        '''

        # Make sure the player can play
        if player != self.get_current_turn():
            raise ValueError(
                type(player), 'It is not {0}\'s turn'.format(player))

        # Copy the state to create a new TicTacToe state
        new_state = np.copy(self.board)
        new_state.flat[move] = player

        # Create and return the next game state
        return TicTacToe(board=new_state, turn=self.players[0])

    def get_winner(self):
        '''
        Return the player who has won in the current game state, or None if no
        player has won yet
        '''

        # Check the rows for three in a row
        for row in self.board:
            if np.all(row == row[0]) and row[0] != 0:
                return row[0]

        # Check the columns for three in a row
        for col in self.board.T:
            if np.all(col == col[0]) and col[0] != 0:
                return col[0]

        # Check the NW-SE diagonal for three in a row
        if np.all(self.board.diagonal() == self.board.diagonal()[0]) and self.board.diagonal()[0] != 0:
            return self.board.diagonal()[0]

        # Check the NE-SW diagonal for three in a row
        flipped_diagonal = np.fliplr(self.board).diagonal()
        if np.all(flipped_diagonal == flipped_diagonal[0]) and flipped_diagonal[0] != 0:
            return flipped_diagonal[0]

        # Return None since there is not yet a winner
        return None

    def __str__(self):
        '''
        Returns a human-readable string representation of the game state
        '''

        string = ''

        for v, row in enumerate(self.board):
            string += ' ' + ' | '.join(row) + '\n'
            if v != len(self.board)-1:
                string += '+'.join([('-' * 3) for i in row])


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
