#JMJ
#RandomAI.py
#Computer program which makes random moves.
#Section programmed by Aaron Bangs

import random
import numpy
import keras

from py_checkers.game import Move
from py_checkers.agent import Agent


class LearningAI(Agent):
    def select_move(self, board):
        self.board = board
        pass

    def preprocess(self, board): #Processes a board to be formatted in Portable Draughts Notation, where it returns an array, with each position in the array marking one possible position on the board, holding a value of 1 for the current player and -1 for the opponent.
        processed_data = [0]*32
        for p in board.grid:
            if p.color == self.color.other:
                val = -1
            elif p.color == self.color:
                val = 1
            x = p.x
            y = p.y
            processed_data[(y*4 + (x//2 + 1))-1] = val
        return processed_data

    def to_coords(self, pdn): #Changes from PDN to coords
        #IF PIECES ARE ON "EVEN" SQUARES (starting at 0,0), which is incorrect
        #order = [0,2,4,6,1,3,5,7]
        #IF PIECES ARE ON "ODD" SQUARES (starting at 1,0)
        order = [1,3,5,7,0,2,4,6]
        x = order[(pdn-1) % 8]
        y = ((pdn-1) // 4)
        return(x,y)

    def to_move(self, pdn_loc_from, pdn_loc_to, board): #Returns a Move() object when given data in Portable Droughts Notation

        x1, y1 = self.to_coords(pdn_loc_from)
        x2, y2 = self.to_coords(pdn_loc_to)
        
        return Move(board.getPieceAt(x1,y1), x2, y2)

    
            

"""

            return selectedMove
        
"""
