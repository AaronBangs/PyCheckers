#JMJ
#RandomAI.py
#Computer program which makes random moves.
#Section programmed by Gerard Pepin

from PyCheckers import *
from Agent import Agent
import random

class RandomAI(Agent):

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
        pieceArray = self.getAllPieces(board)
        #Places all movable pieces into an array.
        for i in pieceArray:
            for move in board.getPossibleMoves(piece):
                moveArray.append(move)
        return moveArray

    def selectMove(self, board):
        while True:
            moveArray = self.getAllMoves(board)
            selectedMove = random.choice(moveArray)
            if selectedMove.piece.color == self.color:
                return selectedMove
            else:
                continue
    
    def shouldDoubleJump(self, board, piece):
        return True

    def selectDoubleJump(self, board, piece):
        while True:
            moveArray = board.getPossibleMoves(piece)
            selectedMove = random.choice(moveArray)
            if selectedMove.piece.color == color and selectedMove.isJump(board):
                return selectedMove
            else:
                continue
        
