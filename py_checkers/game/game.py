#JMJ
#CheckerGame.py
#Contains everything you need for a basic game of checkers.
#Programmed by Ben Campbell

from py_checkers.game import Board, Player
import os, copy

class CheckerGame():
    def __init__(self, black_agent, red_agent, prints_on=True):
        self.black_player = black_agent
        self.red_player = red_agent
        self.board = Board()
        self.is_over = False
        self.winner = None
        self.current_player = black_agent
        self.prints_on = prints_on

    @property
    def next_player(self):
        if self.current_player.color == Player.black:
            return self.red_player
        else:
            return self.black_player

    def play(self, prints=False):
        MAX_TURNS = 150
        
        
        if prints:
            if str(type(self.black_player)) == "<class 'AaronAI.AaronAI'>":
                print("Player %i" % (self.black_player.id_num), end='')
            if str(type(self.red_player)) == "<class 'AaronAI.AaronAI'>":
                print(" vs Player %i" % self.red_player.id_num, end='')
            print()

        num_of_turns = 0

        while not self.is_over:
            
            os.system('cls')
            
            if self.current_player.color == Player.black:
                if self.prints_on: print("Black's turn!")
            elif self.current_player.color == Player.red:
                if self.prints_on: print("red's turn!")

            if self.prints_on: print(self.board)

            if str(type(self.current_player)) == "<class 'AaronAI.AaronAI'>":
                move = self.current_player.select_move(self.board, 2)
            else:
                move = self.current_player.select_move(self.board)

            self.apply_move(move)
            num_of_turns += 1
            if num_of_turns > MAX_TURNS:
                break

            if self.is_over:
                break
            

            #check for double jump
            while move.is_jump(self.board) and self.board.piece_can_jump(move.piece) and self.current_player.should_double_jump(self.board, move.piece):
                new_move = self.current_player.select_double_jump(self.board, move.piece)
                if new_move.is_jump(self.board):
                    move = new_move
                    self.apply_move(move)
                else:
                    print("That's not a jump.")
                    continue

            self.current_player = self.next_player
        
        if self.winner is Player.black:
            print("Black Wins!")
        else:
            print("red Wins!")

    def play_silently(self):
        while not self.is_over:
            move = self.current_player.select_move(self.board)
            self.apply_move(move)
            if self.is_over:
                break

            #check for double jump
            while move.is_jump(self.board) and self.board.piece_can_jump(move.piece) and self.current_player.should_double_jump(self.board, move.piece):
                new_move = self.current_player.select_double_jump(self.board, move.piece)
                if new_move.is_jump(self.board):
                    move = new_move
                    self.apply_move(move)

            self.current_player = self.next_player

        return self.winner

    def apply_move(self, move):
        if move == None:
            if self.current_player.color == Player.black:
                self.winner = Player.black
            else:
                self.winner = Player.red
            
            self.is_over = True
            return

        move.play(self.board)


    def get_state(self):
        '''
        returns a deep copy of the game so you can record it's state while still
        being able to play on. This is probably inefficient.
        '''
        return copy.deep_copy(self)
