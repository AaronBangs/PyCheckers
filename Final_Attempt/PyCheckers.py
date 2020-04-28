#JMJ
#PyCheckers.py
#Contains everything you need for a basic game of checkers.
#Programmed mostly by Aaron Bangs with a little help from Ben Campbell

import enum
import numpy

class Player(enum.Enum):
    black = 1
    white = 2

    @property
    def other(self):
        return Player.black if self == Player.white else Player.white #Returns the opposite color from what it is called from; by Aaron

class Piece():
    def __init__(self, x, y, color): #Initializes the position, color and kingship of a piece; by Aaron
        self.x = x
        self.y = y
        self.color = color
        self.isKing = False

    def __repr__ (self): # by Aaron
        return 'Piece (x: ' + str(self.x) + ' | y: ' + str(self.y) + ' | color: ' + str(self.color)[7:] + ' | king: ' + str(self.isKing) + ')'

    def __eq__(self, other):
        if other == None:
            return False
        if self.x == other.x and self.y == other.y and self.color == other.color: #Does NOT check to see if the king status is the same; by Aaron
            return True
        return False

    def makeKing(self): #by Aaron
        self.isKing = True

class Move():
    def __init__(self, piece, to_x, to_y): #Initializes the piece, and the x and y the piece will be moving to; by Aaron
        self.piece = piece
        self.to_x = to_x
        self.to_y = to_y

        self.delta_x = self.to_x - self.piece.x
        self.delta_y = self.to_y - self.piece.y
        self.direction = (numpy.sign(self.delta_x), numpy.sign(self.delta_y)) #The direction the piece is moving in, as a tuple
        assert abs(self.direction[0]) == abs(self.direction[1]) #Make sure it's on a diagonal! If not, don't even bother continuing

        self.capture = Piece(self.piece.x + self.direction[0], self.piece.y + self.direction[1], self.piece.color.other)
        
        #FOR DEBUGGING PURPOSES
        #print(self)
        
    
    def isValid(self, board): #Checks to see if the move is valid on a given board; by Aaron, modified by Ben
        onBoard = board.withinBounds(self.to_x, self.to_y) #The move does not go off of the board
        spaceIsEmpty = not board.occupied(self.to_x, self.to_y) #There is not a piece occupying the space being moved to
        moveIsSingle = abs(self.delta_x) == 1 and abs(self.delta_y) == 1  #Move is not a jump
        moveIsJump = abs(self.delta_x) == 2 and abs(self.delta_y) == 2  #If move is a jump
        enemyInMiddle = board.find(self.capture) #Make sure there is a piece of the opposite color in the next space
        isForward = self.piece.isKing \
            or (self.piece.color == Player.black and self.direction[1] == 1) \
            or (self.piece.color == Player.white and self.direction[1] == -1)
        
        return onBoard and spaceIsEmpty and (moveIsSingle or (moveIsJump and enemyInMiddle)) and isForward
    
    def isJump(self, board): #You should always make sure the move is valid BEFORE calling this to check if it is a jump; by Aaron
        return (abs(self.delta_x) == 2 and abs(self.delta_y) == 2)

    def play(self, board): #Plays the move on the specified board, if it is valid; by Aaron
        if self.isValid(board): #If the move is valid on the given board
            if self.isJump(board):
                p = board.find(self.capture)
                board.remove(p)

            #print(str(self))
            self.piece.x = self.to_x
            self.piece.y = self.to_y
            
            if (self.piece.y == 7 and self.piece.color == Player.black) or (self.piece.y == 0 and self.piece.color == Player.white):
                self.piece.makeKing() #Make the piece a king if it reaches the end of the board
            
        else:
            print("Move is invalid. \n" + str(self))

    #def __repr__(self):
    #    return str('Piece: ' + str(self.piece) + '\n To x: ' + str(self.to_x) + '\n To y: ' + str(self.to_y) + '\n Delta x: ' + str(self.delta_x) + '\n Delta y: ' + str(self.delta_y) + '\n Direction: ' + str(self.direction) + '\n Capture (if jump): ' + str(self.capture) + '\n')
    
    def __repr__(self):
        return "(%i, %i) -> (%i, %i)" %(self.piece.x, self.piece.y, self.to_x, self.to_y)
        
class Board():
    def __init__(self, blank=False):

        self.WIDTH = 8
        self.HEIGHT = 8
        
        self.grid = []

        for y in range(0,self.HEIGHT): #Adds the first pieces onto the board; by Aaron
            for x in range(0,self.WIDTH):
                if (x + y - 1)%2 == 0:
                    if y < 3:
                        self.grid.append(Piece(x, y, Player.black))
                    elif y > 4:
                        self.grid.append(Piece(x, y, Player.white))

    def find(self, piece): #Checks if there is a specific piece on the board; by Aaron
        for p in self.grid:
            if p == piece:
                return p
            
    def occupied(self, x, y): #Checks if there is any piece at position x, y; by Aaron
        for p in self.grid:
            if p.x == x and p.y == y:
                #print("Space occupied: (%i, %i)" % (x, y))
                return True
        return False

    def remove(self, piece): #by Aaron
        try:
            self.grid.remove(piece)
        except:
            print("Could not remove piece: " + str(piece))
            pass

    def getPieceAt(self, x, y): #by Ben
        for piece in self.grid:
            if piece.x == x and piece.y == y:
                return piece
        print("Could not find piece at location (%i, %i)" % (x, y))
        return None

    def movePieceTo(self, piece, x, y): #by Aaron
        move = Move(piece, x, y)
        move.play(self)

    def withinBounds(self, x, y): #by Aaron
        if x < 0 or x > (self.WIDTH - 1) or y < 0 or y > (self.HEIGHT - 1):
            #print("(%i, %i) is outside Board." % (x, y))
            return False
        return True
    
    def getPossibleMoves(self, piece): #by Gerard
        moves = \
            [
            Move(piece, piece.x - 2, piece.y - 2),\
            Move(piece, piece.x + 2, piece.y - 2),\
            Move(piece, piece.x - 2, piece.y + 2),\
            Move(piece, piece.x + 2, piece.y + 2),\
            Move(piece, piece.x - 1, piece.y - 1),\
            Move(piece, piece.x + 1, piece.y - 1),\
            Move(piece, piece.x - 1, piece.y + 1),\
            Move(piece, piece.x + 1, piece.y + 1)
            ]

        #print(moves)

        validMoves = []
        
        for move in moves:
             if move.isValid(self):
                 validMoves.append(move)

        return validMoves
    
    def getAllPossibleMoves(self, color):
        pieces = list(filter(lambda p: p.color == color, self.grid))
        moves = []

        jumpIsPossible = False
        for p in pieces:
            piece_moves = self.getPossibleMoves(p)
            moves.extend(piece_moves)
            if not jumpIsPossible:
                for m in piece_moves:
                    if m.isJump(self):
                        jumpIsPossible = True

        if jumpIsPossible:
            moves = list(filter(lambda m: m.isJump(self), moves))
        
        return moves

    def pieceCanJump(self, piece):
        upLeft      = Move(piece, piece.x - 2, piece.y - 2).isValid(self)
        upRight     = Move(piece, piece.x + 2, piece.y - 2).isValid(self)
        downLeft    = Move(piece, piece.x - 2, piece.y + 2).isValid(self)
        downRight   = Move(piece, piece.x + 2, piece.y + 2).isValid(self)

        if piece.isKing: return upLeft or upRight or downLeft or downRight
        elif piece.color == Player.white: return upLeft or upRight
        elif piece.color == Player.black: return downLeft or downRight

    def pieceCanMove(self, piece):
        valid = False
        
        upLeft      = Move(piece, piece.x - 1, piece.y - 1).isValid(self)
        upRight     = Move(piece, piece.x + 1, piece.y - 1).isValid(self)
        downLeft    = Move(piece, piece.x - 1, piece.y + 1).isValid(self)
        downRight   = Move(piece, piece.x + 1, piece.y + 1).isValid(self)

        if piece.isKing: valid = upLeft or upRight or downLeft or downRight
        elif piece.color == Player.white: valid = upLeft or upRight
        elif piece.color == Player.black: valid = downLeft or downRight
        
        return self.pieceCanJump(piece) or valid

    def __str__(self): #by Aaron
        out = ''
        
        print('   0  1  2  3  4  5  6  7 ') #Print the numbers to indicate x positions
        
        for y in range(0,8):
            
            out += str(y) + ' ' #Print the numbers to indicate y positions, and a space to make it legible
            
            for x in range(0,8):
                
                if (x+y-1)%2 == 0:
                    addchr = '   ' #Add black squares to the appropriate places (this is meant for dark mode) 
                else:
                    addchr = '███' #Add white squares to the appropriate places
                
                for p in self.grid: #Loops through each piece in the grid every time... there may be a more efficient way of doing this
                    if p.x == x and p.y == y: #If the x and y of the piece matches the x and y being appended to the output string
                        if p.color == Player.white: #If it is white
                            if p.isKing:
                                addchr = ' ■ ' #A piece appears as square if it is a king
                            else:
                                addchr = ' ● '
                        elif p.color == Player.black: #If it is black
                            if p.isKing:
                                addchr = ' □ '
                            else:
                                addchr = ' ○ '
                out += addchr #Add the desired character to the grid
                
            out += '\n'
        return out



#for debugging purposes:
"""
b = Board()
print(b)
p = b.getPieceAt(2,2)
b.movePieceTo(p,3,3)
print(b)
p = b.getPieceAt(5,5)
b.movePieceTo(p,4,4)
print(b)
p = b.getPieceAt(3,3)
b.movePieceTo(p,5,5)
print(b)
p = b.getPieceAt(7,1)
b.movePieceTo(p,8,2)
print(b)
p = b.getPieceAt(4,2)
b.movePieceTo(p,5,3)
print(b)
p = b.getPieceAt(4,6)
b.movePieceTo(p,6,4)
print(b)
b.movePieceTo(p,4,2)
print(b)
"""
