#JMJ
#HumanVsRandom.py
#Plays a game of checkers between two humans
#Programmed by Ben Campbell and Aaron Bangs

from CheckerGame import CheckerGame
from Human import Human
from AaronAI import AaronAI
from RandomAI import RandomAI
from PyCheckers import Player
from Loader import Loader
import random

def __main__():
    
    selection = random.randint(0,9)
    
    blackPlayer = AaronAI(Player.black, selection)
    whitePlayer = Human(Player.white)

    game = CheckerGame(blackPlayer, whitePlayer)
    game.play()

__main__()
