# Allow recursive annotations. Sucks this isn't default until 3.10
from __future__ import annotations

from abc import ABC, abstractmethod, abstractstaticmethod

import numpy

import ConsoleQuestionPrompts as questions

TIE = DRAW = 'DRAW'


class Player:
    def __init__(self, side, board: GameState, user_input_cast: function):
        self.side = side
        self.user_input_cast = user_input_cast

    def get_move(self, possible_moves):
        pass


class HumanPlayer(Player):
    def get_move(self, possible_moves):
        return questions.ask_question(prompt='It is {0}\'s turn. What is your move? '.format(self.side),
                                      in_bounds=lambda move: move in possible_moves,
                                      cast=self.user_input_cast,
                                      error='Invalid move! Possible moves include {0}'.format(possible_moves[:5]))


class GameState(ABC):
    '''
    A base class to store the generic state of any game at a single point in
    time
    '''

    @abstractstaticmethod
    def parse_user_input():
        pass

    def __init__(self):
        self.players = []

    @abstractmethod
    def get_state(self):
        '''
        Returns the current state of the game
        '''
        pass

    @abstractmethod
    def get_current_turn(self):
        '''
        Returns the player whose turn it currently is
        '''
        pass

    def next_turn(self):
        self.players.append(self.players.pop(0))

    @abstractmethod
    def get_possible_moves(self, player):
        '''
        Returns the list of available moves to the given player

        Arguments:

            player      The player who wants to make a move
        '''

        pass

    @abstractmethod
    def move(self, player, move) -> GameState:
        '''
        Advances the game state by making the given move by the given player

        Arguments:

            player      The player who is making the move

            move        The move made to advance the game

        Returns:
            The new game state
        '''

        pass

    @abstractmethod
    def get_winner(self):
        '''
        Returns the winner of the game when the current state of the game has
        reached a win condition

        Returns None if there is not yet a winner
        '''

        pass

    @abstractmethod
    def is_finished(self) -> bool:
        '''
        Returns true if the game has ended in this current state, regardless of
        whether there is a winner.
        '''
        pass

    def get_score(self, player):
        '''
        Gets the current score for the given player, if they have a score

        Arguments:

            player      The player whose score is requested
        '''

        pass

    def concede(self, player):
        '''
        Make the given player concede the game

        Arguments:

            player      The player who wishes to concede the game
        '''

        pass

    @abstractmethod
    def __str__(self):
        return super().__str__()
