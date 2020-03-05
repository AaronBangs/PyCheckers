#JMJ
#RandomAI.py
#Computer program which makes random moves.
#Section programmed by Gerard Pepin

from PyCheckers import *
from Agent import Agent
import random

class Random(Agent):
    def selectMove(self, board):
        piece = None
        pieceArray = []
        moveArray = []
        while piece == None:
            for eachPiece in board.grid:
                if board.pieceCanMove(eachPiece):
                    pieceArray.append(eachPiece)
        #Places all movable pieces into an array.
        for i in pieceArray:
            for move in getPossibleMove(piece):
                moveArray.append(move)

        return random.choice(moveArray)
    
    def shouldDoubleJump(self, board, piece):
        return True

    def selectDoubleJump(self, board, piece):
        
        
        

        
        
        
