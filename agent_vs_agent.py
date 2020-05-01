from py_checkers.game import CheckerGame, Player
from py_checkers.agent import Human, RandomAI

def __main__():
    black_player = Human(Player.black)
    white_player = Human(Player.red)

    game = CheckerGame(black_player, white_player)
    game.play()

__main__()