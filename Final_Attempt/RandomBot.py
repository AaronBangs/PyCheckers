# +JMJ+
# AgentBot.py
# An class to have our randomAI play games with other bots. This does not actually play a game,
# it just communicates with a game that's already being run.
#
# Programmed by Ben Campbell

from Bot import Bot
from PyCheckers import Player, Board, Move
from RandomAI import RandomAI

class RandomBot(Bot):

    def __init__(self, color, botFolder):
            if (color == "black"):
                color = Player.black
            else:
                color = Player.white

            self.board = Board()
            self.agent = RandomAI(color)

    @staticmethod
    def coordsToString(x, y):
        """ converts coordinates into a string like 2x3 """
        return str(x) + "x" + str(y)

    @staticmethod
    def stringToCoords(string):
        """ converts a string like 2x3 into a tuple like (2, 3) """
        coords = string.split('x')
        return (int(coords[0]), int(coords[1]))

    def makemove(self):
        """
        Returns a tuple. The first is the piece that's moving
        The second item is an array that contains the posiitions it
        ends up in or the steps in a multiple jump.
        """
        moveList = []
        piecePosition = ""

        move = self.agent.selectMove(self.board)
        if (move == None):
            return "resign"

        moveList.append(self.coordsToString(move.to_x, move.to_y))
        piecePosition = self.coordsToString(move.piece.x, move.piece.y)

        move.play(self.board)

        while move.isJump(self.board) and self.board.pieceCanJump(move.piece) and self.agent.shouldDoubleJump(self.board, move.piece):
                newMove = self.agent.selectDoubleJump(self.board, move.piece)
                if newMove.isJump(self.board):
                    move = newMove
                    move.play(self.board)
                    moveList.append(self.coordsToString(move.to_x, move.to_y))
                else:
                    print("That's not a jump.")
                    continue

        print(piecePosition, moveList)

        return (piecePosition, moveList)

    def receiveMove(self, move):
        """
        Receives a move from the other bot and applies it to
        to its own gamestate.

        If it receives an invalid move, it returns False.

        Else, it returns true.
        """
        piece_x, piece_y = self.stringToCoords(move[0])
        moveList = move[1]

        piece = self.board.getPieceAt(piece_x, piece_y)

        if not self.board.pieceCanMove(piece):
                print("That piece can't move")
                return False

        for move in moveList:
            to_x, to_y = RandomBot.stringToCoords(move)
            if not self.board.withinBounds(to_x, to_y):
                print("That's not on the board, silly")
                return False
            move = Move(piece, to_x, to_y)
            if not move.isValid(self.board):
                print("That is not a valid move")
                return False
            move.play(self.board)
            # print(self.board)

        return True
pass
