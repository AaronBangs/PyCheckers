#JMJ
#CheckerGame.py
#Contains everything you need for a basic game of checkers.
#Programmed by Ben Campbell

from PyCheckers import Board, Player
import os, copy

class CheckerGame():
    def __init__(self, blackAgent, whiteAgent):
        self.blackPlayer = blackAgent
        self.whitePlayer = whiteAgent
        self.board = Board()
        self.isOver = False
        self.winner = None
        self.currentPlayer = blackAgent

    @property
    def next_player(self):
        if self.currentPlayer.color == Player.black:
            return self.whitePlayer
        else:
            return self.blackPlayer

    def play(self):

        while not self.isOver:
            
            os.system('cls')
            
            if self.currentPlayer.color == Player.black:
                print("Black's turn!")
            elif self.currentPlayer.color == Player.white:
                print("White's turn!")

            print(self.board)

            move = self.currentPlayer.selectMove(self.board)

            self.applyMove(move)

            if self.isOver:
                break

            #check for double jump
            while move.isJump(self.board) and self.board.pieceCanJump(move.piece) and self.currentPlayer.shouldDoubleJump(self.board, move.piece):
                newMove = self.currentPlayer.selectDoubleJump(self.board, move.piece)
                if newMove.isJump(self.board):
                    move = newMove
                    self.applyMove(move)
                else:
                    print("That's not a jump.")
                    continue

            self.currentPlayer = self.next_player
        
        if self.winner is Player.black:
            print("Black Wins!")
        else:
            print("White Wins!")

    def playSilently(self):
        while not self.isOver:
            move = self.currentPlayer.selectMove(self.board)
            self.applyMove(move)
            if self.isOver:
                break

            #check for double jump
            while move.isJump(self.board) and self.board.pieceCanJump(move.piece) and self.currentPlayer.shouldDoubleJump(self.board, move.piece):
                newMove = self.currentPlayer.selectDoubleJump(self.board, move.piece)
                if newMove.isJump(self.board):
                    move = newMove
                    self.applyMove(move)

            self.currentPlayer = self.next_player

        return self.winner

    def applyMove(self, move):
        if move == None:
            if self.currentPlayer.color == Player.black:
                self.winner = Player.black
            else:
                self.winner = Player.white
            
            self.isOver = True
            return

        move.play(self.board)


    def getState(self):
        '''
        returns a deep copy of the game so you can record it's state while still
        being able to play on. This is probably inefficient.
        '''
        return copy.deepcopy(self)
