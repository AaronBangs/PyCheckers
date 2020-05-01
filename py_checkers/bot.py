# +JMJ+
# AgentBots.py
# A modue with classes to have our agents play games with other bots. These do not actually 
# play a game, it just communicates with a game that's already being run.
#
# Programmed by Ben Campbell

import copy
from py_checkers.ai_api import Bot
from py_checkers.game import Player, Board, Move
from py_checkers.agent import RandomAI, MonteCarloAI

class AgentBot(Bot):
    """
    The class that translates from Agents to bots.

    Example tree: 
    Agent->RandomAI;
    Bot->AgentBot->RandomBot;
    RandomBot has it's own instance of RandomAI to make moves.
    """

    def __init__(self, Agent):
            self.board = Board()
            self.agent = Agent
            self.last_board_state = None

    @staticmethod
    def coords_to_string(x, y):
        """ converts coordinates into a string like 2x3 """
        return str(x+1) + "x" + str(8-y)

    @staticmethod
    def string_to_coords(string):
        """ converts a string like 2x3 into a tuple like (2, 3) """
        coords = string.split('x')
        return (int(coords[0])-1, 8-int(coords[1]))

    def make_move(self):
        """
        Returns a tuple. The first is the piece that's moving
        The second item is an array that contains the posiitions it
        ends up in or the steps in a multiple jump.
        """
        
        self.last_board_state = copy.deepcopy(self.board)

        move_list = []
        piece_position = ""

        move = self.agent.select_move(self.board)
        if (move == None):
            return "resign"

        piece_was_not_king = not move.piece.is_king

        move_list.append(self.coords_to_string(move.to_x, move.to_y))
        piece_position = self.coords_to_string(move.piece.x, move.piece.y)

        move.play(self.board)

        piece_is_now_king = move.piece.is_king
        if piece_was_not_king and piece_is_now_king:
            return (piece_position, move_list)

        while move.is_jump(self.board) and self.board.piece_can_jump(move.piece) and self.agent.should_double_jump(self.board, move.piece):
                new_move = self.agent.select_double_jump(self.board, move.piece)
                if new_move.is_jump(self.board):
                    move = new_move
                    move.play(self.board)
                    move_list.append(self.coords_to_string(move.to_x, move.to_y))

                    piece_is_now_king = move.piece.is_king
                    if piece_was_not_king and piece_is_now_king:
                        break
                else:
                    print("That's not a jump.")
                    continue

        print(piece_position, move_list)

        return (piece_position, move_list)

    def receive_move(self, move):
        """
        Receives a move from the other bot and applies it to
        to its own gamestate.

        If it receives an invalid move, it returns False.

        Else, it returns true.
        """
        piece_x, piece_y = self.string_to_coords(move[0])
        move_list = move[1]

        piece = self.board.get_piece_at(piece_x, piece_y)

        if piece.color is self.agent.color:
            print("That's my piece, not yours!")
            return False

        if not self.board.piece_can_move(piece):
                print("That piece can't move")
                return False

        for move in move_list:
            to_x, to_y = self.string_to_coords(move)
            if not self.board.within_bounds(to_x, to_y):
                print("That's not on the board, silly")
                return False
            move = Move(piece, to_x, to_y)
            if not move.is_valid(self.board):
                print("That is not a valid move")
                return False
            move.play(self.board)
            # print(self.board)

        return True

    def undo_last_move(self):
        """
        called when the other bot returns false for recieve_move. This is sent to the
        bot who made the move, telling it to undo the last move it made. If the last move
        had several jumps, all of them are undone, so the board is in the same state it
        was in before the move was made.
        """
        self.board = self.last_board_state

    def get_board_str(self):
        return str(self.board)

class RandomBot(AgentBot):
    def __init__(self, color):
        if (color == "black"):
            color = Player.black
        else:
            color = Player.red

        agent = RandomAI(color)
        super().__init__(agent)


SECONDS_CALCULATING = 2
TEMPERATURE = 1.5

class MonteCarloBot(AgentBot):
    def __init__(self, color):
        if (color == "black"):
            color = Player.black
        else:
            color = Player.red

        agent = MonteCarloAI(color, SECONDS_CALCULATING, TEMPERATURE)
        super().__init__(agent)

 