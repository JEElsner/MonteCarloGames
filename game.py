# Allow recursive annotations. Sucks this isn't default until 3.10
from __future__ import annotations

from abc import ABC, abstractmethod

import numpy

from vectorize_objects import vectorize

TIE = DRAW = 'DRAW'


def main():
    import questions

    import tic_tac_toe
    import othello

    games = {'Tic Tac Toe': tic_tac_toe, 'Othello': othello}

    choice = questions.option_question(
        'Which game would you like to play?', games.keys(), list(games.values()))

    game_types = ['All AI', 'Player vs AI', 'Player vs Player']
    n_humans = questions.option_question('Who will be playing?', game_types)

    players = []
    for i in range(n_humans):
        players.append(HumanPlayer)

    while len(players) < 2:
        players.append(MonteCarloPlayer)

    for state in choice.create_game_and_get_game_loop(players):
        pass


class Player:
    def __init__(self, side, board: GameState):
        self.side = side

    def get_move(self, possible_moves):
        pass

    def notify_move(self, move, side):
        pass


class HumanPlayer(Player):
    def get_move(self, possible_moves):
        move = int(input('Place {0} where? '.format(self.side)))

        if move not in possible_moves:
            print('Invalid move!')
            return self.get_move(possible_moves)
        else:
            return move

    def notify_move(self, move, side):
        pass


class MonteCarloPlayer(Player):
    def __init__(self, side, board: GameState):
        from monte_carlo import Node

        super().__init__(side, board)

        self.base_node = Node(board)
        self.curr_node = self.base_node

    def get_move(self, possible_moves):
        print('Thinking...')
        # print(len(self.curr_node.children))
        try:
            return self.curr_node.get_move()
        except RuntimeWarning:
            pass

    def notify_move(self, move, side):
        self.curr_node = self.curr_node.next_state(move, side)


class GameState(ABC):
    '''
    A base class to store the generic state of any game at a single point in
    time
    '''

    def __init__(self):
        self.players = []

        # Create v_funcs for this object
        vectorize(GameState)

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


if __name__ == '__main__':
    main()
