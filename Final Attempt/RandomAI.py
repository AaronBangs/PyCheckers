#JMJ
#RandomAI.py
#Computer program which makes random moves.
#Section programmed by Gerard Pepin

from PyCheckers import *
from Agent import Agent
import random

class Random(Agent):

    def getAllPieces(self, board):
        piece = None
        pieceArray = []
        moveArray = []
        while piece == None:
            for eachPiece in board.grid:
                if board.pieceCanMove(eachPiece):
                    pieceArray.append(eachPiece)
        return pieceArray
    
    def getAllMoves(self, board):
        pieceArray = getAllPieces(board)
        #Places all movable pieces into an array.
        for i in pieceArray:
            for move in board.getPossibleMoves(piece):
                moveArray.append(move)
        return moveArray

    def selectMove(self, board):
        moveArray = getAllMoves(board)

        return random.choice(moveArray)
    
    def shouldDoubleJump(self, board, piece):
        return True

    def selectDoubleJump(self, board, piece):
