import ConsoleQuestionPrompts as questions
import datetime
import pickle

from . import *

file_extension = '.pickle'


def main():
    games = {'Tic Tac Toe': TicTacToe, 'Othello': Othello}

    choice: type = questions.option_question(
        'Which game would you like to play?', games.keys(), list(games.values()))

    game_types = ['All AI', 'Player vs AI', 'Player vs Player']
    n_humans = questions.option_question('Who will be playing?', game_types)

    players = []
    for i in range(n_humans):
        players.append(HumanPlayer)

    while len(players) < 2:
        players.append(MonteCarloPlayer)

    played_game = MonteCarloTree(choice, players)

    rounds = [(0, played_game.current_state)]
    print(played_game.current_state)

    for move, state in played_game.play_rounds():
        rounds.append((move, state))
        print(state)

        if state.is_finished():
            if state.get_winner() is not game.DRAW:
                print(state.get_winner(), 'wins!')
            else:
                print('The game is a draw!')

    if questions.yes_no_question('Save this game? '):
        name = questions.ask_question('Game name: ')

        filename = '-'.join([choice.__name__, name,
                             datetime.datetime.now().strftime('%Y_%m_%d_%H%M')]) + file_extension

        with open(filename, mode='wb') as file:
            pickle.dump(rounds, file)
            print('Game saved as', filename)


if __name__ == '__main__':
    main()
