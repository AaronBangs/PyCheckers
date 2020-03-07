#JMJ
#CheckerGame.py
#Contains everything you need for a basic game of checkers.
#Programmed by Ben Campbell

from PyCheckers import *
import os

class CheckerGame():
    def __init__(self, blackAgent, whiteAgent):
        self.board = Board()
        self.isOver = False
        self.blackPlayer = blackAgent
        self.whitePlayer = whiteAgent

    def play(self):
        currentPlayer = self.blackPlayer

        while not self.isOver:
            
            os.system('cls')
            
            if currentPlayer.color == Player.black:
                print("Black's turn!")
            elif currentPlayer.color == Player.white:
                print("White's turn!")

            print(self.board)

            move = currentPlayer.selectMove(self.board)

            if move == None:
                if currentPlayer.color == Player.black:
                    print("White wins!")
                else:
                    print("Black wins!")
                
                self.isOver = True
                break
            
            move.play(self.board)

            #check for double jump
            while move.isJump(self.board) and self.board.pieceCanJump(move.piece) and currentPlayer.shouldDoubleJump(self.board, move.piece):
                newMove = currentPlayer.selectDoubleJump(self.board, move.piece)
                if newMove.isJump(self.board):
                    move = newMove
                    move.play(self.board)
                else:
                    print("That's not a jump.")
                    continue

            if currentPlayer.color == Player.black:
                currentPlayer = self.whitePlayer
            else:
                currentPlayer = self.blackPlayer
            
