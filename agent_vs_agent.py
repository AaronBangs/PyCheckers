from py_checkers.game import CheckerGame, Player
from py_checkers.agent import Human, RandomAI

def __main__():
    blackPlayer = Human(Player.black)
    whitePlayer = Human(Player.white)

    game = CheckerGame(blackPlayer, whitePlayer)
    game.play()

__main__()