#JMJ
#Agent.py
#An interface to make moves in a game of checkers.
#Programmed by Ben Campbell

class Agent:
    
    def __init__(self, color):
        self.color = color

    def getAllPieces(self, board):#Aaron
        pieceArray = []
        moveArray = []
        for eachPiece in board.grid:
            if board.pieceCanMove(eachPiece) and eachPiece.color == self.color:
                pieceArray.append(eachPiece)
        return pieceArray
    
    def getAllMoves(self, board):#Aaron
        pieceArray = self.getAllPieces(board)
        #Places all movable pieces into an array.
        moveArray = []
        for piece in pieceArray:
            for move in board.getPossibleMoves(piece):
                moveArray.append(move)
        return moveArray

    def selectMove(self, board):
        '''returns a move'''
        raise NotImplementedError()

    def shouldDoubleJump(self, board, piece):
        return True

    def selectDoubleJump(self, board, piece):
        '''returns a move after a double jump'''
        raise NotImplementedError()
