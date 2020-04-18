#JMJ
#HumanVsRandom.py
#Plays a game of checkers between two humans
#Programmed by Ben Campbell

from CheckerGame import CheckerGame
from Human import Human
from RandomAI import RandomAI
from PyCheckers import Player

def __main__():
    blackPlayer = RandomAI(Player.black)
    whitePlayer = Human(Player.white)

    game = CheckerGame(blackPlayer, whitePlayer)
    game.play()

__main__()
