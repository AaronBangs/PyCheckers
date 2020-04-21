#JMJ
#HumanVsMonteCarlo.py
#Plays a game of checkers between you and a MonteCarlo Bot
#Programmed by Ben Campbell

from CheckerGame import CheckerGame
from Human import Human
from MonteCarloAI import MonteCarloAI
from PyCheckers import Player

def __main__():
    whitePlayer = Human(Player.white)
    blackPlayer = MonteCarloAI(Player.black, 70, 1.5)

    game = CheckerGame(blackPlayer, whitePlayer)
    game.play()

__main__()
