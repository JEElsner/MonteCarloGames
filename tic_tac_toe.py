from __future__ import annotations

import numpy as np
import os

import game
from game import GameState

from vectorize_objects import vectorize

import monte_carlo as mct
from monte_carlo import Node


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

    def get_state(self) -> np.ndarray:
        '''
        Returns the state of the game board
        '''
        return self.board

    def get_current_turn(self) -> str:
        '''
        Returns the player whose turn it currently is. (Players are 'X' and 'O')
        '''
        return self.players[0]

    def get_possible_moves(self, player) -> np.ndarray:
        '''
        Return the possible moves as a list of integers as the index of each
        square in the Tic-Tac-Toe grid.
        '''
        if player != self.get_current_turn():
            return np.empty(0)

        return np.arange(self.board.size)[np.char.isdigit(self.board.flat)]

    def move(self, player, move) -> TicTacToe:
        '''
        Returns a new TicTacToe object representing the next state of the game
        after this move is made.

        Arguments:

            player      The player who is making this move

            move        The integer representing the index of the square to
                        place the player's piece
        '''

        # Make sure it's the player's turn
        if player != self.get_current_turn():
            raise ValueError(
                type(player), 'It is not {0}\'s turn'.format(player))

        # Make sure the move is allowed
        if move not in self.get_possible_moves(player):
            raise ValueError(move, 'Invalid move')

        # Copy the state to create a new TicTacToe state
        new_state = np.copy(self.board)
        new_state.flat[move] = player

        # Create and return the next game state
        return TicTacToe(board=new_state, turn=self.players[1])

    def get_winner(self) -> str:
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

        if np.all(np.char.isalpha(self.get_state())):
            return game.TIE

        # Return None since there is not yet a winner
        return None

    def is_finished(self) -> bool:
        return self.get_winner() is not None or \
            np.all(np.char.isalpha(self.get_state()))

    def __str__(self):
        '''
        Returns a human-readable string representation of the game state
        '''

        string = ''

        for v, row in enumerate(self.board):
            string += ' ' + ' | '.join(row) + ' \n'
            if v != len(self.board)-1:
                string += '+'.join([('-' * 3) for i in row]) + '\n'

        return string


def create_game_and_get_game_loop(players):
    game_board = TicTacToe()

    players = {'X': players[0]('X', game_board),
               'O': players[1]('O', game_board)}

    end = False
    winner = None
    while not end:
        side = game_board.get_current_turn()
        player = players[side]

        print(str(game_board))

        location = player.get_move(game_board.get_possible_moves(side))
        game_board = game_board.move(player.side, location)

        for watcher in players.values():
            watcher.notify_move(location, player.side)

        if game_board.is_finished():
            break

        yield game_board

    print(str(game_board))

    if game_board.get_winner() is not game.DRAW:
        print(game_board.get_winner(), 'wins!')
    else:
        print('The game is a draw!')


if __name__ == '__main__':
    for state in create_game_and_get_game_loop([game.HumanPlayer, game.MonteCarloPlayer]):
        pass
