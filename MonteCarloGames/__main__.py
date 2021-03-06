import ConsoleQuestionPrompts as questions

from . import *


def main():
    games = {'Tic Tac Toe': TicTacToe, 'Othello': Othello}

    choice = questions.option_question(
        'Which game would you like to play?', games.keys(), list(games.values()))

    game_types = ['All AI', 'Player vs AI', 'Player vs Player']
    n_humans = questions.option_question('Who will be playing?', game_types)

    players = []
    for i in range(n_humans):
        players.append(HumanPlayer)

    while len(players) < 2:
        players.append(MonteCarloPlayer)

    played_game = MonteCarloTree(choice, players)

    for state in played_game.play_rounds():
        print(state)

        if state.is_finished():
            if state.get_winner() is not game.DRAW:
                print(state.get_winner(), 'wins!')
            else:
                print('The game is a draw!')


if __name__ == '__main__':
    main()
