#JMJ
#Human.py
#A way for humans to play checkers.
#Programmed by Ben Campbell

from py_checkers.game import Move
from py_checkers.agent import Agent

class Human(Agent):
    
    def select_move(self, board):

        if Agent.get_all_moves(board, self.color) == []:
            return None
        
        # select a piece
        piece = None
        while piece == None:
            try: #Try / except added by Aaron to avoid crashes
                from_x = int(input("from x:"))
            except:
                print("Invalid entry. Try again.")
                continue
            try:
                from_y = int(input("from y:"))
            except:
                print("Invalid entry. Try again.")
                continue

            if not board.within_bounds(from_x, from_y):
                print("That's not on the board, silly")
                continue
            if not board.occupied(from_x, from_y):
                print("There is no piece at (%i, %i)" % (from_x, from_y))
                continue
            if board.get_piece_at(from_x, from_y).color != self.color:
                print("That piece is the wrong color")
                continue

            

            piece = board.get_piece_at(from_x, from_y)

            if not board.piece_can_move(piece):
                print("That piece can't move")
                piece = None
                continue

        # get the destination
        move = None
        while move == None:
            try:
                to_x = int(input("to x:"))
            except:
                print("Invalid entry. Try again.")
                continue
            try:
                to_y = int(input("to y:"))
            except:
                print("Invalid entry. Try again.")
                continue

            if not board.within_bounds(to_x, to_y):
                print("That's not on the board, silly")
                continue
            move = Move(piece, to_x, to_y)
            if not move.is_valid(board):
                print("That is not a valid move")
                move = None
                continue
        
        return move

    def should_double_jump(self, board, piece):
        answer = input("Would you like to double jump (y/n):")
        if answer == 'y':
            return True
        return False

    def select_double_jump(self, board, piece):
        print (board)

        # get the destination
        move = None
        while move == None:
            to_x = int(input("to x:"))
            to_y = int(input("to y:"))

            if not board.within_bounds(to_x, to_y):
                print("That's not on the board, silly")
                continue
            move = Move(piece, to_x, to_y)
            if not move.is_valid(board):
                print("That is not a valid move")
                move = None
                continue
        
        return move
