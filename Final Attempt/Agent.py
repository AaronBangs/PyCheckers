#JMJ
#Agent.py
#An interface to make moves in a game of checkers.

class Agent:
    def __init__(self, color):
        self.color = color

    def selectMove(self, board):
        '''returns a move'''
        raise NotImplementedError()

    def shouldDoubleJump(self, board, piece):
        return True

    def selectDoubleJump(self, board, piece):
        '''returns a move after a double jump'''
        raise NotImplementedError()