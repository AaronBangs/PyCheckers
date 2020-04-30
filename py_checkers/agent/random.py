#JMJ
#RandomAI.py
#Computer program which makes random moves.
#Section programmed by Gerard Pepin

from py_checkers.agent import Agent
import random

class RandomAI(Agent):
    
    def select_move(self, board):
        while True:
            moveArray = board.getAllPossibleMoves(self.color)
            if moveArray == []:
                return None
            selectedMove = random.choice(moveArray)
            # print("\n\nSelected Move: " + str(selectedMove) + "\n\n")
            return selectedMove
    
    def should_double_jump(self, board, piece):
        return True

    def select_double_jump(self, board, piece):
        while True:
            moveArray = board.getPossibleMoves(piece)
            jumpArray = []
            
            for move in moveArray:
                if move.isJump(board):
                    jumpArray.append(move)
            
            #print("Jump array: " + str(jumpArray))
            
            selectedMove = random.choice(jumpArray)

            # print("-> (%i, %i)" %(selectedMove.to_x, selectedMove.to_y))
            
            return selectedMove
        
