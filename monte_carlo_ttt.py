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

    def __init__(self, side, board):
        '''
        Creates the Monte Carlo Node.

        Arguments:

            side        The player that just made a move to reach this game state

            board       The current state of the game represented by this node
        '''

        self.state = board
        self.side = side

        self.wins = 0
        self.total = 0

        self.children = {}

        # Create v_funcs for all object methods
        vectorize(Node)

    def win_rate(self):
        '''
        Returns the probability of winning for the player that made the move to
        get to this game state.
        '''

        return np.divide(self.wins, self.total)

    def next_state(self, move, side):
        '''
        Returns the next valid state after the state represented by this node.
        The new returned state is reached from the current game state when the
        passed side makes the passed move

        Arguments:

            move        The move made to reach the new game state

            side        The player that makes the move to get to the new game
                        state
        '''

        # Expand the game-state tree if necessary
        if move not in self.children.keys():
            new_state = np.copy(self.state)
            new_state.flat[move] = side

            # Add the copy of the game state
            self.children.update(
                {move: Node(-1 * self.side, new_state)})

        # Return the game state reached by move
        return self.children[move]

    def is_end(self):
        '''
        Determines whether the node is a terminal leaf node that cannot be
        extended with more moves: i.e. the contained game state is likely the
        end of a game

        Returns:

            False if a move can be made,
            True otherwise.
        '''

        # TODO this is pretty garbage and maybe a little repetative, fix this

        is_won = get_winner(self.state) != None
        return is_won | np.count_nonzero(self.state) == self.state.size

    def weight(self, parent_node_explored, exploration_param=np.sqrt(2)):
        '''
        Returns the weight of the node for how likely it is to be chosen to be
        explored during simulations
        '''

        return np.divide(self.wins, self.total) + exploration_param * \
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
        if self.is_end():
            return

        # If there are no game states simulated after the current one, create them
        if len(self.children) == 0:
            self.expand()

        # Simulate moves as long as there is more than one option
        if len(self.children) > 1:
            begin = datetime.datetime.now()
            while datetime.datetime.now() - begin < decision_time:
                self.explore()

        # Sort the possible moves by their likelyhood of leading to a win
        # TODO: this is actually pretty good, but it feels bad
        win_rates = {n.win_rate(): move for move, n in self.children.items()}

        # Debug *ahem* diagnostic statements
        # print(list(self.children.values())[0].side)
        # print(self.total)

        # for m, n in self.children.items():
        #     print(m, ':', n.wins, n.total)

        # Return the move with the highest likelyhood of leading to a win
        return win_rates[max(win_rates.keys())]

    def expand(self):
        '''
        Adds children as possible game states resulting from moves made from the
        current game state but does not simulate the probabilities of winning
        for these moves.
        '''

        # Add a move for each open board position
        for i in range(self.state.size):
            if self.state.flat[i] == 0:
                new_state = np.copy(self.state)
                new_state.flat[i] = -1 * self.side

                self.children.update(
                    {i: Node(-1 * self.side, new_state)})

    def explore(self):
        '''
        Randomly samples win states for moves made branching from this game
        state (Monte Carlo Method).
        '''

        self.total += 1  # Increment total number of simulations on this node

        winner = get_winner(self.state)
        # Base case
        if winner != None:
            pass
            # We don't return out of the function yet, because even for the base
            # case there is still some work to be done (at the bottom of the function)
        # Other base case
        elif np.count_nonzero(self.state) == self.state.size:
            winner = 0  # Set the win state to a tie
        else:  # Recursive case

            # If there aren't any simulated moves beyond this one, generate them
            if len(self.children) == 0:
                self.expand()

            # Choose the node to explore
            weights = Node.v_weight(
                np.array(list(self.children.values())), self.total)

            # If there are any unsimulated branches, only choose among them
            if np.any(np.isnan(weights)):
                weights[~np.isnan(weights)] = 0
                weights[np.isnan(weights)] = 1

            # Choose a branch to explore weighted by their priority
            node = rng.choice(list(self.children.values()),
                              p=weights/weights.sum())

            # explore node
            winner = node.explore()

        # Record result (for both the base case and the recursive case)
        self.wins += int(winner == self.side or winner == 0)
        return winner  # Return the winner so higher up nodes can record their win_rate
