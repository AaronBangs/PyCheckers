#JMJ
#AaronAI.py
#Computer program which moves a little smartly.
#Section programmed by Gerard Pepin and Aaron Bangs

from PyCheckers import *
from Agent import Agent
from Loader import *
import random
import copy

class AaronAI(Agent):

    def __init__(self, color, id_num = 0):
        
        self.color = color
        
        NUMBER_OF_WEIGHTS = 8

        self.id_num = id_num

        #try to load the weightArray from a file
        weightArray = Loader.loadArray(self.id_num)
        #if it doesn't load:
        if weightArray == []:
            weightArray.append(1.0) #Starts at the 1st generation
            for x in range(1, NUMBER_OF_WEIGHTS+1): #Starts at 1 so that it doesn't include the generation number
                weightArray.append(random.random())
        
        Loader.saveArray(self.id_num, weightArray)

        self.weightArray = weightArray
        
    def tweak(self, amount):
        self.weightArray[0] += 1
        for x in range(1, len(self.weightArray)):
            x += random.random() * amount * random.choice([-1,1])
            if x < 0:
                x = 0
            if x > 1:
                x = 1
        Loader.saveArray(self.id_num, self.weightArray)

    def evaluate(self, board, move, weightArray, depth):
        move_value = 0
        
        if move.isValid(board) and move.isJump(board):
                move_value += weightArray[0]#

        newBoard = copy.deepcopy(board)
        copyMove = copy.deepcopy(move)
        

        if copyMove.isValid(newBoard):
            
            copyMove.play(newBoard)
            piece = copyMove.piece
            
            if newBoard.pieceCanJump(piece):
                move_value += weightArray[1]#
                if copyMove.isJump(newBoard):
                    move_value += weightArray[2]#

            if not newBoard.pieceCanMove(piece):
                move_value -= weightArray[3]#

                for neighbor in piece.neighbors(newBoard):
                    if neighbor != None and neighbor.color != self.color and newBoard.pieceCanJump(neighbor):
                        move_value -= weightArray[4]#
                        neq = board.getPieceAt(neighbor.x, neighbor.y)
                        if not board.pieceCanJump(neq):
                            move_value += weightArray[5]#
            if depth > 0:
                guesser = AaronAI(self.color.other, self.id_num)
                guess = guesser.selectMove(newBoard, 0)
                if guess != None: guess.play(newBoard)
                move_value += self.evaluate(newBoard, copyMove, weightArray, depth-1) * depth / weightArray[6]#

            del piece
        

        del newBoard
        del copyMove
        
                        
        if not move.piece.isKing:
             move_value += weightArray[7]#

        return move_value
        

    def choose(self, board, moves, weightArray, depth):
        
        valueArray = [0] * len(moves)
        
        for move in moves:
            if move.isValid(board):
                valueArray[moves.index(move)] = self.evaluate(board, move, weightArray, depth)
            else:
                valueArray[moves.index(move)] = -100
            
        returnArray = []
        threshold = max(valueArray)
        for x in range(len(valueArray)):
            if valueArray[x] >= threshold:
                returnArray.append(moves[x])

        #print("\n", threshold)
        
        return random.choice(returnArray)
            
    
    def selectMove(self, board, depth):
        while True:
            moveArray = self.getAllMoves(board)
            if moveArray == []:
                return None
            selectedMove = self.choose(board, moveArray, self.weightArray[1:], depth)
            #print("\n\nSelected Move: " + str(selectedMove) + "\n\n")
            return selectedMove
    
    def shouldDoubleJump(self, board, piece):
        return True

    def selectDoubleJump(self, board, piece):
        while True:
            moveArray = board.getPossibleMoves(piece)
            jumpArray = []
            
            for move in moveArray:
                if move.isJump(board):
                    jumpArray.append(move)
            
            #print("Jump array: " + str(jumpArray))
            
            selectedMove = self.choose(board, jumpArray, self.weightArray[1:], 1)

            #print("-> (%i, %i)" %(selectedMove.to_x, selectedMove.to_y))
            
            return selectedMove
        
