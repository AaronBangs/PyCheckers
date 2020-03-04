import enum
from collections import namedtuple

class Player(enum.Enum):
    black = 1
    white = 2

    @property
    def other(self):
        return Player.black if self == Player.white else Player.white

class Piece():
    def __init__ (self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.isKing = False

    def __repr__ (self):
        return 'Piece (x: ' + str(self.x) + ' | y: ' + str(self.y) + ' | color: ' + str(self.color)[7:] + ' | king: ' + str(self.isKing) + ')'

    def makeKing(self):
        self.isKing = True
