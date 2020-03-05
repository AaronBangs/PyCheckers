#JMJ
#Human.py
#A way for humans to play checkers.

from PyCheckers import *
from Agent import Agent

class Human(Agent):
    def selectMove(self, board):
        # select a piece
        piece = None
        while piece == None:
            from_x = int(input("from x:"))
            from_y = int(input("from y:"))

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