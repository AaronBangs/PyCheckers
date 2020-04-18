#JMJ
#RandomAI.py
#Computer program which makes random moves.
#Section programmed by Gerard Pepin

from Agent import Agent
import random

class RandomAI(Agent):
    
    def selectMove(self, board):
        while True:
            moveArray = Agent.getAllMoves(board, self.color)
            if moveArray == []:
                return None
            selectedMove = random.choice(moveArray)
            # print("\n\nSelected Move: " + str(selectedMove) + "\n\n")
            return selectedMove
    
    def shouldDoubleJump(self, board, piece):
        return random.choice([True, False])

    def selectDoubleJump(self, board, piece):
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
        
