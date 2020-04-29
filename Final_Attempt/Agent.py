#JMJ
#Agent.py
#An interface to make moves in a game of checkers.
#Programmed by Ben Campbell

class Agent:
    
    def __init__(self, color):
        self.color = color

    @staticmethod
    def getAllPieces(board, color):#Aaron
        pieceArray = []
        for eachPiece in board.grid:
            if board.pieceCanMove(eachPiece) and eachPiece.color == color:
                pieceArray.append(eachPiece)
        return pieceArray
    
    @staticmethod
    def getAllMoves(board, color):#Aaron
        pieceArray = Agent.getAllPieces(board, color)
        #Places all movable pieces into an array.
        moveArray = []
        for piece in pieceArray:
            for move in board.getPossibleMoves(piece):
                moveArray.append(move)
        return board.getAllPossibleMoves(color)

    def selectMove(self, board):
        '''returns a move'''
        raise NotImplementedError()

    def shouldDoubleJump(self, board, piece):
        return True

    def selectDoubleJump(self, board, piece):
        '''returns a move after a double jump'''
        raise NotImplementedError()
