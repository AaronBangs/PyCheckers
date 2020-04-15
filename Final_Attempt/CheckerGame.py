#JMJ
#CheckerGame.py
#Contains everything you need for a basic game of checkers.
#Programmed by Ben Campbell

from PyCheckers import *
import os

class CheckerGame():
    def __init__(self, blackAgent, whiteAgent, prints_on=True):
        self.board = Board()
        self.isOver = False
        self.blackPlayer = blackAgent
        self.whitePlayer = whiteAgent
        self.prints_on = prints_on

    def play(self, prints=False):
        MAX_TURNS = 150
        
        
        currentPlayer = self.blackPlayer

        if prints:
            if str(type(self.blackPlayer)) == "<class 'AaronAI.AaronAI'>":
                print("Player %i" % (self.blackPlayer.id_num), end='')
            if str(type(self.whitePlayer)) == "<class 'AaronAI.AaronAI'>":
                print(" vs Player %i" % self.whitePlayer.id_num, end='')
            print()

        num_of_turns = 0
        
        while not self.isOver:
            
            if self.prints_on: os.system('cls')
            
            if currentPlayer.color == Player.black:
                if self.prints_on: print("Black's turn!")
            elif currentPlayer.color == Player.white:
                if self.prints_on: print("White's turn!")

            if self.prints_on: print(self.board)

            if str(type(currentPlayer)) == "<class 'AaronAI.AaronAI'>":
                move = currentPlayer.selectMove(self.board, 2)
            else:
                move = currentPlayer.selectMove(self.board)


            if move == None:
                if currentPlayer.color == Player.black:
                    if self.prints_on: print("White wins!")
                    return Player.white
                else:
                    if self.prints_on: print("Black wins!")
                    return Player.black
                
                self.isOver = True
                break
            
            move.play(self.board)
            num_of_turns += 1
            if num_of_turns > MAX_TURNS:
                return None

            #check for double jump
            while move.isJump(self.board) and self.board.pieceCanJump(move.piece) and currentPlayer.shouldDoubleJump(self.board, move.piece):
                newMove = currentPlayer.selectDoubleJump(self.board, move.piece)
                if newMove.isJump(self.board):
                    move = newMove
                    move.play(self.board)
                else:
                    if self.prints_on: print("That's not a jump.")
                    continue

            if currentPlayer.color == Player.black:
                currentPlayer = self.whitePlayer
            else:
                currentPlayer = self.blackPlayer
            
