#JMJ
#Agent.py
#An interface to make moves in a game of checkers.
#Programmed by Ben Campbell

class Agent:
    
    def __init__(self, color):
        self.color = color

    @staticmethod
    def get_all_pieces(board, color):#Aaron
        pieceArray = []
        for eachPiece in board.grid:
            if board.piece_can_move(eachPiece) and eachPiece.color == color:
                pieceArray.append(eachPiece)
        return pieceArray
    
    @staticmethod
    def get_all_moves(board, color):#Aaron
        pieceArray = Agent.get_all_pieces(board, color)
        #Places all movable pieces into an array.
        moveArray = []
        for piece in pieceArray:
            for move in board.get_all_possible_moves(piece):
                moveArray.append(move)
        return board.get_all_possible_moves(color)

    def select_move(self, board):
        '''returns a move'''
        raise NotImplementedError()

    def should_double_jump(self, board, piece):
        return True

    def select_double_jump(self, board, piece):
        '''returns a move after a double jump'''
        raise NotImplementedError()
