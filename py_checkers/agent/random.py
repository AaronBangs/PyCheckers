#JMJ
#RandomAI.py
#Computer program which makes random moves.
#Section programmed by Gerard Pepin

from py_checkers.agent import Agent
import random

class RandomAI(Agent):
    
    def select_move(self, board):
        while True:
            move_array = board.get_all_possible_moves(self.color)
            if move_array == []:
                return None
            selected_move = random.choice(move_array)
            # print("\n\nSelected Move: " + str(selected_move) + "\n\n")
            return selected_move
    
    def should_double_jump(self, board, piece):
        return True

    def select_double_jump(self, board, piece):
        while True:
            move_array = board.get_possible_moves(piece)
            jump_array = []
            
            for move in move_array:
                if move.is_jump(board):
                    jump_array.append(move)
            
            #print("Jump array: " + str(jump_array))
            
            selected_move = random.choice(jump_array)

            # print("-> (%i, %i)" %(selected_move.to_x, selected_move.to_y))
            
            return selected_move
        
