from CheckerTypes import *
import numpy as np
#from Helper import *

class Move():
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
    def __init__(self): #by Aaron
        self.width = 8
        self.height = 8

        self._grid = [] #Here "grid" is a list which stores all of the active pieces.
        
        #For loop to initialize grid
        for y in range(0,8):
            for x in range(0,8):
                if y == 0 or  y == 2: #The coordinates here are to ensure a checker-board pattern
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

    def movePieceTo(self, piece, x, y):
        assert self.is_on_grid(x, y)
        assert self.getPieceAt(x, y) is None # make sure the space is empty
        dx = x - piece.x
        dy = y - piece.y
        assert abs(dx) == abs(dy) # make sure it is diagonal
        # if make sure it is forward (black = down(+), white = up(-)) for non kings
        if not piece.isKing:
            if piece.color is Player.black:
                assert np.sign(dy) == 1
            elif piece.color is Player.white:
                assert np.sign(dy) == -1
        assert abs(dy) <= 2 # make sure it is single or jump
        # if it is a jump, make sure there is an enemy piece in the middle
        if abs(dy) == 2:
            middleX = piece.x + np.sign(dx)
            middleY = piece.y + np.sign(dy)
            middlePiece = self.getPieceAt(middleX, middleY)
            assert middlePiece is not None
            assert piece.color is not middlePiece.color
            # remove the piece in the middle
            self._grid.remove(middlePiece)
        # move the piece
        piece.x = x
        piece.y = y
        # make it a king if needed (black = y 7, white = y 0)
        if not piece.isKing:
            if (piece.color is Player.black and piece.y == 7) or (piece.color is Player.white and piece.y == 0):
                piece.makeKing()

    def getPieceAt(self, x, y):
        for piece in self._grid:
            if piece.x == x and piece.y == y:
                return piece
        return None

    def is_on_grid(self, x, y):
        return x >= 0 and x <= self.width and y >= 0 and y <= self.height

    def moveIsJump(self, piece, x, y):
        dx = x - piece.x
        dy = y - piece.y
        if abs(dy) == 2:
            middleX = piece.x + np.sign(dx)
            middleY = piece.y + np.sign(dy)
            middlePiece = self.getPieceAt(middleX, middleY)
            if middlePiece is not None and piece.color is not middlePiece.color:

                return True
        return False

    
    def pieceCanJump(self, piece): #by Aaron
        
        p1p1 = self.getPieceAt(piece.x+1,piece.y+1) 
        p1m1 = self.getPieceAt(piece.x+1,piece.y-1)
        m1p1 = self.getPieceAt(piece.x-1,piece.y+1)
        m1m1 = self.getPieceAt(piece.x-1,piece.y-1)

        p2p2 = self.getPieceAt(piece.x+2,piece.y+2) 
        p2m2 = self.getPieceAt(piece.x+2,piece.y-2)
        m2p2 = self.getPieceAt(piece.x-2,piece.y+2)
        m2m2 = self.getPieceAt(piece.x-2,piece.y-2)
        
        """
        Defines the pieces at these positions, if they exist
            m2m2████    ████p2m2
            ████m1m1████p1m1████
                ████piec████
            ████m1p1████p1p1████
            m2p2████    ████p2p2
        """
        


        
        if piece.isKing:
            if (p2p2 == None and p1p1 != None and p1p1.color != piece.color)\
                or (p2m2 == None and p1m1 != None and p1m1.color != piece.color)\
                or (m2m2 == None and m1m1 != None and m1m1.color != piece.color)\
                or (m1p1 == None and m1p1 != None and m1p1.color != piece.color):
                return True
            '''
            Makes sure at least one of the jump-to spaces is available with a piece of the opposite color in between the current piece and it.

             x ███   ███ x  
            ███ ○ ███ ○ ███
               ███ ■ ███
            ███ ○ ███ ○ ███
             x ███   ███ x

            One of the 4 jumps marked by the x must be possible to return True
            '''
                    
        else: #If the piece is not a king
            if piece.color == Player.white:
                if (m2m2 == None and m1m1 != None and m1m1.color != piece.color)\
                    or (p2m2 == None and p1m1 != None and p1m1.color != piece.color):
                    return True
            """
             x ███   ███ x  
            ███ ○ ███ ○ ███
               ███ ● ███

            only looking for these here
            """


            
            if piece.color == Player.black:
                if (p2p2 == None and p1p1 != None and p1p1.color != piece.color)\
                    or (m2p2 == None and m1p1 != None and m1p1.color != piece.color):
                    return True


            """
               ███ ○ ███
            ███ ● ███ ● ███
             x ███   ███ x

            only looking for these here
            """

        return False #Only if all the tests above fail

    def __str__(self): #by Aaron
        out = ''
        
        print('   0  1  2  3  4  5  6  7 ') #Print the numbers to indicate x positions
        
        for y in range(0,8):
            
            out += str(y) + ' ' #Print the numbers to indicate y positions, and a space to make it legible
            
            for x in range(0,8):
                
                if (x+y)%2 == 0:
                    addchr = '   ' #Add black squares to the appropriate places (this is meant for dark mode) 
                else:
                    addchr = '███' #Add white squares to the appropriate places
                
                for p in self._grid: #Loops through each piece in the grid every time... there may be a more efficient way of doing this
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
'''
class GameState:
    def __init__(self, board, next_player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        if self.previous_state is None:
            self.previous_states = frozenset()
        else:
            self.previous_states = frozenset(
                previous.previous_states |
                {(previous.next_player, previous.board.zobrist_hash())})
        self.last_move = move

    def apply_move(self, move):
        """Return the new GameState after applying the move."""
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, self, move)

    @classmethod
    def new_game(cls, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)

    def is_move_self_capture(self, player, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        new_string = next_board.get_go_string(move.point)
        return new_string.num_liberties == 0

    @property
    def situation(self):
        return (self.next_player, self.board)

    def does_move_violate_ko(self, player, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board.zobrist_hash())
        return next_situation in self.previous_states

    def is_valid_move(self, move):
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        return (
            self.board.get(move.point) is None and
            not self.is_move_self_capture(self.next_player, move) and
            not self.does_move_violate_ko(self.next_player, move))

    def is_over(self):
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass

    def legal_moves(self):
        moves = []
        for x in range(1, self.board.width + 1):
            for y in range(1, self.board.height + 1):
                move = Move.play(Point(x, y))
                if self.is_valid_move(move):
                    moves.append(move)
        # These two moves are always legal.
        moves.append(Move.pass_turn())
        moves.append(Move.resign())

        return moves

    def winner(self):
        if not self.is_over():
            return None
        if self.last_move.is_resign:
            return self.next_player
        game_result = compute_game_result(self)
        return game_result.winner
'''
