import enum
from collections import namedtuple

class Player(enum.Enum):
    black = 1
    white = 2

    @property
    def other(self):
        return Player.black if self == Player.white else Player.white

class Piece():
    def __init__ (self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

