#JMJ
#Human.py
#A way for humans to play checkers.
#Programmed by Ben Campbell

from PyCheckers import *
from Agent import Agent

class Human(Agent):
    
    def selectMove(self, board):

        if Agent.getAllMoves(board, self.color) == []:
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

            if not board.withinBounds(from_x, from_y):
                print("That's not on the board, silly")
                continue
            if not board.occupied(from_x, from_y):
                print("There is no piece at (%i, %i)" % (from_x, from_y))
                continue
            if board.getPieceAt(from_x, from_y).color != self.color:
                print("That piece is the wrong color")
                continue

            

            piece = board.getPieceAt(from_x, from_y)

            if not board.pieceCanMove(piece):
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

            if not board.withinBounds(to_x, to_y):
                print("That's not on the board, silly")
                continue
            move = Move(piece, to_x, to_y)
            if not move.isValid(board):
                print("That is not a valid move")
                move = None
                continue
        
        return move

    def shouldDoubleJump(self, board, piece):
        answer = input("Would you like to double jump (y/n):")
        if answer == 'y':
            return True
        return False

    def selectDoubleJump(self, board, piece):
        print (board)

        # get the destination
        move = None
        while move == None:
            to_x = int(input("to x:"))
            to_y = int(input("to y:"))

            if not board.withinBounds(to_x, to_y):
                print("That's not on the board, silly")
                continue
            move = Move(piece, to_x, to_y)
            if not move.isValid(board):
                print("That is not a valid move")
                move = None
                continue
        
        return move
