#JMJ
#CheckerGame.py
#Contains everything you need for a basic game of checkers.

from PyCheckers import *

class CheckerGame():
    def __init__(self, blackAgent, whiteAgent):
        self.board = Board()
        self.isOver = False
        self.blackPlayer = blackAgent
        self.whitePlayer = whiteAgent

    def play(self):
        currentPlayer = self.blackPlayer

        while not self.isOver:
            if currentPlayer.color == Player.black:
                print("Black's turn!")
            elif currentPlayer.color == Player.white:
                print("White's turn!")

            print(self.board)

            move = currentPlayer.selectMove(self.board)
            move.play(self.board)

            #check for double jump
            while move.isJump(self.board) and self.pieceCanJump(move.piece) and currentPlayer.shouldDoubleJump(self.board, move.piece):
                move = currentPlayer.selectDoubleJump(self.board, move.piece)
                move.play(self.board)

            if currentPlayer.color == Player.black:
                currentPlayer = self.whitePlayer
            else:
                currentPlayer = self.blackPlayer

    def pieceCanJump(self, piece):
        upLeft      = Move(piece, piece.x - 2, piece.y - 2).isValid(self.board)
        upRight     = Move(piece, piece.x + 2, piece.y - 2).isValid(self.board)
        downLeft    = Move(piece, piece.x - 2, piece.y + 2).isValid(self.board)
        downRight   = Move(piece, piece.x + 2, piece.y + 2).isValid(self.board)

        if piece.isKing: return upLeft or upRight or downLeft or downRight
        elif piece.color == Player.white: return upLeft or upRight
        elif piece.color == Player.black: return downLeft or downRight
