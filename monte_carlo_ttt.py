import datetime

import numpy as np
import numpy.random as rng


# NumPy universal functions are extremely handy to use, and I find it increases
# legibility greatly to think of operations as vector operations over vectors.
# Unfortunately, it is impossible to make object methods into vector functions.
#
# This convenience method creates a static v_func for each object method in a
# class. These methods are named v_[method name](). You will see these methods
# used frequently in this code. The method that creates these methods is called
# vectorize(), and you will see it called in object constructors
from vectorize_objects import vectorize

import game
from game import GameState

# Ignore NumPy warnings: namely divide by zero warnings
np.warnings.filterwarnings('ignore')

# The time allowed for the Monte Carlo Tree to explore new game states
decision_time = datetime.timedelta(seconds=2)

# The function into which a gamestate can be passed to determine the winner
# TODO This is horrible, make this better
get_winner = None


class Node:
    '''
    One node in a Monte Carlo Tree. Stores a single game state.
    Information is stored about the probability of winning with the move
    played to reach this game state.
    '''

    def __init__(self, state: GameState, side=None, prev_move=None):
        '''
        Creates the Monte Carlo Node.

        Arguments:

            side        The player that just made a move to reach this game state

            board       The current state of the game represented by this node
        '''

        self.state = state
        self.side = side

        self.wins = 0
        self.total = 0

        self.__previous_move = prev_move

        self.children = []

        # Create v_funcs for all object methods
        vectorize(Node)

    def win_rate(self):
        '''
        Returns the probability of winning for the player that made the move to
        get to this game state.
        '''

        return np.divide(self.wins, self.total)

    @property
    def previous_move(self):
        return self.__previous_move

    def weight(self, parent_node_explored, exploration_param=np.sqrt(2)):
        '''
        Returns the weight of the node for how likely it is to be chosen to be
        explored during simulations
        '''

        return self.win_rate() + exploration_param * \
            np.sqrt(np.divide(np.log(parent_node_explored), self.total))

    def get_move(self):
        '''
        Determines the move where the player who makes it has the highest
        probability of winning. Note that the player or side making this move is
        not the same as the player contained in this node. In games with two
        players, the player contained in this node is the player who has just
        made a move.

        Returns:
            The optimal move estimated by Monte Carlo sampling or
            None if a move cannot be made
        '''

        # Stop if no moves can be made
        if self.state.is_finished():
            return

        # If there are no game states simulated after the current one, create them
        self.expand()

        # Simulate moves as long as there is more than one option
        if len(self.children) > 1:
            begin = datetime.datetime.now()
            while datetime.datetime.now() - begin < decision_time:
                self.explore()

        # Sort the possible moves by their likelyhood of leading to a win
        def sort_key(node): return node.win_rate() \
            if not np.isnan(node.win_rate()) else 0

        # for c in self.children:
        #     print(c.previous_move, c.win_rate())

        self.children.sort(key=sort_key, reverse=True)

        # Return the move with the highest likelyhood of leading to a win
        return self.children[0].previous_move

    def expand(self):
        '''
        Adds children as possible game states resulting from moves made from the
        current game state but does not simulate the probabilities of winning
        for these moves.
        '''

        if len(self.children) == 0:
            # Add a move for each open board position
            for move in self.state.get_possible_moves(self.state.get_current_turn()):
                new_state = self.state.move(
                    self.state.get_current_turn(), move)
                new_node = Node(
                    new_state, side=self.state.get_current_turn(), prev_move=move)
                self.children.append(new_node)

    def explore(self):
        '''
        Randomly samples win states for moves made branching from this game
        state (Monte Carlo Method).
        '''

        self.total += 1  # Increment total number of simulations on this node

        winner = None

        # Base case
        if self.state.is_finished():
            winner = self.state.get_winner()
        else:  # Recursive case

            # If there aren't any simulated moves beyond this one, generate them
            self.expand()

            # Choose the node to explore
            weights = Node.v_weight(self.children, self.total)

            # If there are any unsimulated branches, only choose among them
            if np.any(np.isnan(weights)):
                weights[~np.isnan(weights)] = 0
                weights[np.isnan(weights)] = 1

            # Choose a branch to explore weighted by their priority
            node = rng.choice(self.children, p=weights/weights.sum())

            # explore node
            winner = node.explore()

        # Record result (for both the base case and the recursive case)
        self.wins += int(winner == self.side) + 0.5 * int(winner == game.TIE)
        return winner  # Return the winner so higher up nodes can record their win_rate
