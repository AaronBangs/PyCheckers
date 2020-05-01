# JMJ
# game_state.py
# a new version of game that uses game states instead
# boards are a dictionary of tuples with (x, y) as the key, and (player, isKing) as the value
# Ex: [(0,1):(Player.red, True), (0,3):(Player.black, False), ...]

# python standard library
import copy

# external imports
import numpy as np

# internal imports
from py_checkers.game import Player

_piece_str = ["", " ○ "," ● "," □ "," ■ "] # black, white, black king, white king

def _pdn_to_pos(pdn): #Changes from PDN to coords
        #IF PIECES ARE ON "EVEN" SQUARES (starting at 0,0), which is incorrect
        #order = [0,2,4,6,1,3,5,7]
        #IF PIECES ARE ON "ODD" SQUARES (starting at 1,0)
        order = [1,3,5,7,0,2,4,6]
        x = order[(pdn-1) % 8]
        y = ((pdn-1) // 4)
        return(x,y)

def _pos_to_pdn(x, y): #Returns an integer with a value from 0..31 representing the position on the board of the piece at coordinates (x, y)
   return (y*4 + (x//2 + 1))-1

def _piece_to_int(piece):
  return piece.color + piece.is_king*2


def _moves_to_int(jul, jur, jdl, jdr, ul, ur, dl, dr):
  """ 
  inputs the moves a piece can make as a set of booleans
  outputs an integer from 0 to 255 representing those moves.

  doesn't handle double jumps.

  Moves are in this order:
   0 ███   ███ 1 
  ███ 4 ███ 5 ███
     ███ ■ ███   
  ███ 6 ███ 7 ███
   2 ███   ███ 3 
   the booleans are converted into a string of binary, and then to an int.
   so if piece could move to 0,1, or 6 the int would be 1100010 (0 is left-most, 7 is right-most)

   if the number >= 16, a jump is possible
  """
  return np.packbits(np.array([jul, jur, jdl, jdr, ul, ur, dl, dr]))[0])
  pass

def _shift_board(board, up, left):
  "shifts a board and inserts fives (impassable). Used to calculate moves. negative shifts are valid."
  
  # top and side are arrays of ones that are added on to the board after it's sliced.
  # one represents impassable area.
  if abs(up) == 1:
    top = np.full(8, 5)
  elif up != 0:
    top = np.full((abs(up), 8), 5)
  
  if left != 0:
    side = np.full((8, abs(left)), 5)
  
  shifted_board = board
  
  if up > 0: # shift up
    shifted_board = np.vstack((board[up:, :], top))
  elif up < 0: # shift down
    shifted_board = np.vstack((top, board[:(8+up), :]))
  
  if left > 0: # shift left
    shifted_board = np.hstack((shifted_board[:, left:], side))
  elif left < 0: # shift right
    shifted_board = np.hstack((side, shifted_board[:, :(8-left)]))
  
  return shifted_board


class GameState:
  def __init__(self, moving_player=Player.black, board=None, possible_moves=None):
    if board is None:
      board = GameState.get_starting_board()
    self.board = board
    self.moving_player = moving_player
    pass

  @staticmethod
  def get_starting_board():
    board = [1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2]
    return board

  def get_board_str(self):
    out = ''
    out += '   0  1  2  3  4  5  6  7 \n' # x positions
    
    for y in range(0,8):
      out += str(y) + ' ' # y positions
      
      for x in range(0,8):
        if (x+y-1)%2 == 0:
          addchr = '   ' # black squares
          if self.board[_pos_to_pdn(x, y)] != 0:
            addchr = _piece_str[self.board[_pos_to_pdn(x, y)]]
        else:
          addchr = '███' # white squares
        out += addchr #Add the desired character to the grid
          
      out += '\n'
    return out

    def get_next_state(self, move):
      state = GameState(self.moving_player.other, copy.deepcopy(self.board), copy.deepcopy(self.possible_moves))
      state.update_possible_moves(move)
      return state

  def update_possible_moves(self, move):

    # move the piece
    # add and remove pieces
    # update possible moves for effected pieces
    pass

  def update_all_possible_moves(self):
    jul = _shift_board(board, 2, 2)
    jur = _shift_board(board, 2, -2)
    jdl = _shift_board(board, -2, 2)
    jdr = _shift_board(board, -2, -2)
    ul = _shift_board(board, 1, 1)
    ur = _shift_board(board, 1, -1)
    dl = _shift_board(board, -1, 1)
    dr = _shift_board(board, -1, -1)
