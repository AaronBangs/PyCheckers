from CheckerTypes import *

class Move():  # <1>
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):
        return Move(point=point)

    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)

    @classmethod
    def resign(cls):
        return Move(is_resign=True)

class Board():
    def __init__(self):
        self.num_rows = 8
        self.num_cols = 8

        self._grid = [] #Here "grid" is a list which stores all of the active pieces.
        
        #For loop to initialize grid
        for y in range(0,8):
            for x in range(0,8):
                if y == 0 or  y == 2:
                    if x % 2 == 0:
                        self._grid.append(Piece(x, y, Player.black))
                if y == 1:
                    if (x+1) % 2 == 0:
                        self._grid.append(Piece(x, y, Player.black))

                if y == 5 or y == 7:
                    if (x+1) % 2 == 0:
                        self._grid.append(Piece(x, y, Player.white))
                if y == 6:
                    if x % 2 == 0:
                        self._grid.append(Piece(x, y, Player.white))

                
    def __repr__(self):
        out = ''
        
        for y in range(0,8):
            for x in range(0,8):

                if (x+y)%2 == 0:
                    addchr = '1'
                else:
                    addchr = '0'
                
                for p in self._grid:
                    if p.row == x and p.col == y and p.color == Player.white:
                        addchr = 'w'
                    elif p.row == x and p.col == y and p.color == Player.black:
                        addchr = 'b'
                out += addchr    
                
            out += '\n'
        return out

