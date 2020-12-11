from __future__ import annotations

import numpy as np

import game

import monte_carlo

LIGHT = '\u25CF'  # '\u26AA'
DARK = '\u25CB'  # '\u26AB'

EMPTY = ' '

# Print the coordinates of each square as zero-indexed numbers instead of
# alpha numeric
DEBUG_INDEXES = False

# Different directions of movement represented as a list of
# changes in x and changes in y per space moved. Shown in a square
# pattern hopefully to make it easier to understand
DIRECTIONS = [(-1,  1), (0,  1), (1,  1),
              (-1,  0),          (1,  0),
              (-1, -1), (0, -1), (1, -1)]


def parse_user_input(response: str):
    try:
        return (int(response[1]) - 1)*8 + (ord(response[0].upper()) - 65)
    except:
        return None


def create_game_and_get_game_loop(players):
    game_board = Othello()

    players = {DARK: players[0](DARK, game_board, parse_user_input),
               LIGHT: players[1](LIGHT, game_board, parse_user_input)}

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

        yield game_board

        if game_board.is_finished():
            break

    print(str(game_board))

    if game_board.get_winner() is not game.DRAW:
        print(game_board.get_winner(), 'wins!')
    else:
        print('The game is a draw!')


class Othello(game.GameState):
    def __init__(self, board=None, turn=None):
        shape = (8, 8)  # Create the shape of the board

        self.players = [DARK, LIGHT]  # Identify the players

        if board is None:
            # Create the board
            self.board = np.full(shape, EMPTY, dtype=str, order='F')

            # Place the starting pieces
            self.board[3][3] = DARK
            self.board[4][4] = DARK

            self.board[3][4] = LIGHT
            self.board[4][3] = LIGHT

            # Orientation Debug
            # self.board[0][0] = DARK
            # self.board[7][7] = LIGHT
            # self.board[5][3] = DARK # One possible starting move
        else:
            self.board = board

    def __str__(self) -> str:
        '''
        Give a human-readable version of the othello board. One that visually
        looks like a grid.
        '''
        # Sadly, this function is not human-readable

        # Declare the unicode values for box-drawing characters
        top = '\u2501'
        side = '\u2503'
        corners = {'ul': '\u250F', 'ur': '\u2513',
                   'bl': '\u2517', 'br': '\u251B'}

        # Draw the top edge of the board
        string = '  ' + corners['ul'] + top * \
            self.board.shape[0] + corners['ur'] + '\n'

        # Draw the board
        for y, row in enumerate(reversed(self.board)):
            string += str(self.board.shape[1] - y - DEBUG_INDEXES) + \
                ' ' + side + ''.join(row) + side + '\n'

        # Draw the bottom edge of the board
        string += '  ' + corners['bl'] + top * \
            self.board.shape[0] + corners['br'] + '\n'

        # Draw the indices of the board columns
        string += '   ' + ''.join([chr(65 - (17 * DEBUG_INDEXES) + x)
                                   for x in range(self.board.shape[0])]) + '\n'

        return string

    def get_state(self) -> np.ndarray:
        return self.board

    def get_current_turn(self) -> str:
        return self.players[0]

    def get_possible_moves(self, player: str) -> np.ndarray:
        # Make sure it's the player's turn
        if player != self.get_current_turn():
            return np.empty()

        # Boolean array to track where legal moves can be made
        move_possible = np.zeros(self.board.shape, dtype=bool, order='F')

        # Find moves by iterating through each square, determining if it contains
        # the player's piece, then checking each direction to see if a move can
        # be made flipping the opponent's pieces in that direction
        for y, row in enumerate(self.board):
            for x, square in enumerate(row):

                # Check if player has a piece in that square
                if square == player:
                    for dx, dy in DIRECTIONS:
                        # Expand in each direction until we reach an edge
                        i = 1
                        while 0 < x+dx*i < self.board.shape[1] and \
                                0 < y+dy*i < self.board.shape[0]:

                            if self.board[y+dy*i][x+dx*i] == player:
                                # This direction is broken by one of the
                                # player's pieces, so we can't play here
                                break
                            elif self.board[y+dy*i][x+dx*i] == EMPTY:
                                # By the time we've gotten to this y+dy*i and
                                # x+dx*i, we know we've got an unbroken line of
                                # the enemy's pieces, and now one gap. So this
                                # is a possible move, provided there is at least
                                # one enemy piece between the player's pieces
                                if i > 1:
                                    move_possible[y+dy*i][x+dx*i] = True

                                # We're done searching in this direction
                                break

                            # If none of the above conditions were met, we
                            # haven't found a valid move, but there could still
                            # be a valid move in this direction.
                            #
                            # Increment the counter to continue in the direction
                            i += 1

        # Generate a list labeling each square with an integer, and return
        # only the integers where a move is possible
        indices = np.arange(self.board.size)
        return indices[move_possible.flatten()]

    def move(self, player: str, move) -> Othello:
        '''
        Returns a new Othello object representing the next state of the game
        after this move is made.

        Arguments:

            player      The player who is making this move

            move        The tuple representing the coordinate of the square to
                        place the player's piece
        '''

        # Make sure it's the player's turn
        if player != self.get_current_turn():
            raise ValueError(
                type(player), 'It is not {0}\'s turn'.format(player))

        # Make sure the move is allowed
        if move not in self.get_possible_moves(player):
            raise ValueError(move, 'Invalid move')

        # Copy the state to create a new Othello state
        new_state = np.copy(self.board)
        new_state.flat[move] = player

        # Get the x, y coordinate of the new piece
        xs, ys = np.meshgrid(
            np.arange(self.board.shape[0]), np.arange(self.board.shape[1]), indexing='ij')

        x, y = xs.flat[move], ys.flat[move]

        # Flip all the pieces for the move
        for dx, dy in DIRECTIONS:
            # Expand in each direction until we reach an edge, verifying a
            # possible flip
            i = 1
            flip_good = False

            while 0 < x+dx*i < self.board.shape[1] and \
                    0 < y+dy*i < self.board.shape[0]:

                if self.board[y+dy*i][x+dx*i] == player:
                    # This direction is broken by one of the
                    # player's pieces, so we can't flip here
                    break
                elif self.board[y+dy*i][x+dx*i] == EMPTY:
                    # By the time we've gotten to this y+dy*i and
                    # x+dx*i, we know we've got an unbroken line of
                    # the enemy's pieces, and now one gap. So this
                    # is a possible move, provided there is at least
                    # one enemy piece between the player's pieces
                    if i > 1:
                        flip_good = True

                    # We're done searching in this direction
                    break

                # If none of the above conditions were met, we
                # haven't found a valid move, but there could still
                # be a valid move in this direction.
                #
                # Increment the counter to continue in the direction
                i += 1

            # If the direction just checked can be flipped, flip it
            if flip_good:
                for n in range(i-1, 0, -1):
                    new_state[y+dy*n][x+dx*n] == player

        # Create and return the next game state
        return Othello(board=new_state, turn=self.players[1])

    def get_winner(self) -> str:
        # Return no winner if the game is not finished
        if not self.is_finished():
            return None

        winner = None
        high_score = 0

        # Linear search for winner
        for p in self.players:
            score = np.count_nonzero(self.board == p)
            if score > high_score:
                high_score = score
                winner = p

        return winner

    def is_finished(self):

        # If all the squares are filled, the game is finished
        if np.count_nonzero(self.board) == self.board.size:
            return True

        for player in self.players:

            # If ANY player can make a move, the game is not over
            if len(self.get_possible_moves(player)) != 0:
                return False

        # The last for loop checked if any players can make a move. Since no
        # player can make a move, the game is over.
        return True


def main():
    print(Othello())
    print(Othello().get_possible_moves(DARK))


if __name__ == '__main__':
    for state in create_game_and_get_game_loop([game.HumanPlayer, game.HumanPlayer]):
        pass
