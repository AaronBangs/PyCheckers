#JMJ
#HumanVsMonteCarlo.py
#Plays a game of checkers between you and a MonteCarlo Bot
#Programmed by Ben Campbell

from CheckerGame import CheckerGame
from Human import Human
from MonteCarloAI import MonteCarloAI
from PyCheckers import Player

SIMULATED_GAMES = 2
TEMPERATURE = 1.5

def __main__():
    whitePlayer = Human(Player.white)
    blackPlayer = MonteCarloAI(Player.black, SIMULATED_GAMES, TEMPERATURE)

    game = CheckerGame(blackPlayer, whitePlayer)
    game.play()

__main__()
