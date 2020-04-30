#JMJ
#CheckerGame.py
#Contains everything you need for a basic game of checkers.
#Programmed by Ben Campbell

from py_checkers.game import Board, Player
import os, copy

class CheckerGame():
    def __init__(self, blackAgent, whiteAgent, prints_on=True):
        self.blackPlayer = blackAgent
        self.whitePlayer = whiteAgent
        self.board = Board()
        self.isOver = False
        self.winner = None
        self.currentPlayer = blackAgent
        self.prints_on = prints_on

    @property
    def next_player(self):
        if self.currentPlayer.color == Player.black:
            return self.whitePlayer
        else:
            return self.blackPlayer

    def play(self, prints=False):
        MAX_TURNS = 150
        
        
        if prints:
            if str(type(self.blackPlayer)) == "<class 'AaronAI.AaronAI'>":
                print("Player %i" % (self.blackPlayer.id_num), end='')
            if str(type(self.whitePlayer)) == "<class 'AaronAI.AaronAI'>":
                print(" vs Player %i" % self.whitePlayer.id_num, end='')
            print()

        num_of_turns = 0

        while not self.isOver:
            
            os.system('cls')
            
            if self.currentPlayer.color == Player.black:
                if self.prints_on: print("Black's turn!")
            elif self.currentPlayer.color == Player.white:
                if self.prints_on: print("White's turn!")

            if self.prints_on: print(self.board)

            if str(type(self.currentPlayer)) == "<class 'AaronAI.AaronAI'>":
                move = self.currentPlayer.selectMove(self.board, 2)
            else:
                move = self.currentPlayer.selectMove(self.board)

            self.applyMove(move)
            num_of_turns += 1
            if num_of_turns > MAX_TURNS:
                break

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
