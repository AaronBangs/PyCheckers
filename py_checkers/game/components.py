#JMJ
#PyCheckers.py
#Contains everything you need for a basic game of checkers.
#Programmed mostly by Aaron Bangs with a little help from Ben Campbell

import enum
import numpy

class Player(enum.Enum):
    black = 1
    red = 2

    @property
    def other(self):
        return Player.black if self == Player.red else Player.red #Returns the opposite color from what it is called from; by Aaron

class Piece():
    def __init__(self, x, y, color): #Initializes the position, color and kingship of a piece; by Aaron
        self.x = x
        self.y = y
        self.color = color
        self.is_king = False

    def __repr__ (self): # by Aaron
        return 'Piece (x: ' + str(self.x) + ' | y: ' + str(self.y) + ' | color: ' + str(self.color)[7:] + ' | king: ' + str(self.is_king) + ')'

    def __eq__(self, other):
        if other == None:
            return False
        if type(other) == Piece: # Does NOT check to see if the king status is the same; by Aaron
            if self.x == other.x and self.y == other.y and self.color == other.color: 
                return True
        return super().__eq__(other)

    def make_king(self): #by Aaron
        self.is_king = True

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
    
    def is_valid(self, board): #Checks to see if the move is valid on a given board; by Aaron, modified by Ben
        on_board = board.within_bounds(self.to_x, self.to_y) #The move does not go off of the board
        space_is_empty = not board.occupied(self.to_x, self.to_y) #There is not a piece occupying the space being moved to
        move_is_single = abs(self.delta_x) == 1 and abs(self.delta_y) == 1  #Move is not a jump
        moveis_jump = abs(self.delta_x) == 2 and abs(self.delta_y) == 2  #If move is a jump
        enemy_in_middle = board.find(self.capture) #Make sure there is a piece of the opposite color in the next space
        is_forward = self.piece.is_king \
            or (self.piece.color == Player.black and self.direction[1] == 1) \
            or (self.piece.color == Player.red and self.direction[1] == -1)
        
        return on_board and space_is_empty and (move_is_single or (moveis_jump and enemy_in_middle)) and is_forward
    
    def is_jump(self, board): #You should always make sure the move is valid BEFORE calling this to check if it is a jump; by Aaron
        return (abs(self.delta_x) == 2 and abs(self.delta_y) == 2)

    def play(self, board): #Plays the move on the specified board, if it is valid; by Aaron
        if self.is_valid(board): #If the move is valid on the given board
            if self.is_jump(board):
                p = board.find(self.capture)
                board.remove(p)

            #print(str(self))
            self.piece.x = self.to_x
            self.piece.y = self.to_y
            
            if (self.piece.y == 7 and self.piece.color == Player.black) or (self.piece.y == 0 and self.piece.color == Player.red):
                self.piece.make_king() #Make the piece a king if it reaches the end of the board
            
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

        if blank:
            return

        for y in range(0,self.HEIGHT): #Adds the first pieces onto the board; by Aaron
            for x in range(0,self.WIDTH):
                if (x + y - 1)%2 == 0:
                    if y < 3:
                        self.grid.append(Piece(x, y, Player.black))
                    elif y > 4:
                        self.grid.append(Piece(x, y, Player.red))

    @staticmethod
    def from_string(s):
        """
        converts a string like this to a board:
           0  1  2  3  4  5  6  7 
        0 ███ ○ ███ ○ ███ ○ ███ ○
        1  ○ ███ ○ ███ ○ ███ ○ ███
        2 ███ ○ ███ ○ ███ ○ ███ ○
        3    ███   ███   ███   ███
        4 ███   ███   ███   ███
        5  ● ███ ● ███ ● ███ ● ███
        6 ███ ● ███ ● ███ ● ███ ●
        7  ● ███ ● ███ ● ███ ● ███
        """
        board = Board(True)
        str_array = s.split('\n')
        str_array = str_array[1:] # remove the numbers at the top
        for y, row_str in enumerate(str_array):
            str_array[y] = row_str[1:] # remove the numbers at the right
            str_array[y] = str_array[y].split("███")
            for x, space_str in enumerate(str_array[y]):
                space_str = space_str.strip()

                # get pieces from dots/squares
                if space_str != '':
                    if y%2 == 0: # even rows
                        board.grid.append(Board.str_to_piece(space_str, x*2-1, y))
                    else: # odd rows
                        board.grid.append(Board.str_to_piece(space_str, x*2, y))
        return board

    @staticmethod
    def str_to_piece(s, x, y):
        piece = Piece(x, y, Player.black)
        if s == '●' or s == '■':
            piece.color = Player.red
        if s == '□' or s == '■':
            piece.make_king()
        return piece


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

    def get_piece_at(self, x, y): #by Ben
        for piece in self.grid:
            if piece.x == x and piece.y == y:
                return piece
        print("Could not find piece at location (%i, %i)" % (x, y))
        return None

    def move_piece_to(self, piece, x, y): #by Aaron
        move = Move(piece, x, y)
        move.play(self)

    def within_bounds(self, x, y): #by Aaron
        if x < 0 or x > (self.WIDTH - 1) or y < 0 or y > (self.HEIGHT - 1):
            #print("(%i, %i) is outside Board." % (x, y))
            return False
        return True
    
    def get_possible_moves(self, piece): #by Gerard
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

        valid_moves = []
        
        for move in moves:
             if move.is_valid(self):
                 valid_moves.append(move)

        return valid_moves
    
    def get_all_possible_moves(self, color):
        pieces = list(filter(lambda p: p.color == color, self.grid))
        moves = []

        jump_is_possible = False
        for p in pieces:
            piece_moves = self.get_possible_moves(p)
            moves.extend(piece_moves)
            if not jump_is_possible:
                for m in piece_moves:
                    if m.is_jump(self):
                        jump_is_possible = True

        if jump_is_possible:
            moves = list(filter(lambda m: m.is_jump(self), moves))
        
        return moves

    def piece_can_jump(self, piece):
        up_left      = Move(piece, piece.x - 2, piece.y - 2).is_valid(self)
        up_right     = Move(piece, piece.x + 2, piece.y - 2).is_valid(self)
        down_left    = Move(piece, piece.x - 2, piece.y + 2).is_valid(self)
        down_right   = Move(piece, piece.x + 2, piece.y + 2).is_valid(self)

        if piece.is_king: return up_left or up_right or down_left or down_right
        elif piece.color == Player.red: return up_left or up_right
        elif piece.color == Player.black: return down_left or down_right

    def piece_can_move(self, piece):
        valid = False
        
        up_left      = Move(piece, piece.x - 1, piece.y - 1).is_valid(self)
        up_right     = Move(piece, piece.x + 1, piece.y - 1).is_valid(self)
        down_left    = Move(piece, piece.x - 1, piece.y + 1).is_valid(self)
        down_right   = Move(piece, piece.x + 1, piece.y + 1).is_valid(self)

        if piece.is_king: valid = up_left or up_right or down_left or down_right
        elif piece.color == Player.red: valid = up_left or up_right
        elif piece.color == Player.black: valid = down_left or down_right
        
        return self.piece_can_jump(piece) or valid

    def __str__(self): #by Aaron
        out = ''
        
        out += '   0  1  2  3  4  5  6  7 \n' #Print the numbers to indicate x positions
        
        for y in range(0,8):
            
            out += str(y) + ' ' #Print the numbers to indicate y positions, and a space to make it legible
            
            for x in range(0,8):
                
                if (x+y-1)%2 == 0:
                    addchr = '   ' #Add black squares to the appropriate places (this is meant for dark mode) 
                else:
                    addchr = '███' #Add red squares to the appropriate places
                
                for p in self.grid: #Loops through each piece in the grid every time... there may be a more efficient way of doing this
                    if p.x == x and p.y == y: #If the x and y of the piece matches the x and y being appended to the output string
                        if p.color == Player.red: #If it is red
                            if p.is_king:
                                addchr = ' ■ ' #A piece appears as square if it is a king
                            else:
                                addchr = ' ● '
                        elif p.color == Player.black: #If it is black
                            if p.is_king:
                                addchr = ' □ '
                            else:
                                addchr = ' ○ '
                out += addchr #Add the desired character to the grid
                
            out += '\n'
        return out
