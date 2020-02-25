from CheckerTypes import *

class Move():  # <1>
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):
        return Move(point=point)

    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)

    @classmethod
    def resign(cls):
        return Move(is_resign=True)

class Board():
    def __init__(self):
        self.num_rows = 8
        self.num_cols = 8

        self._grid = [] #Here "grid" is a list which stores all of the active pieces.
        
        #For loop to initialize grid
        for y in range(0,8):
            for x in range(0,8):
                if y == 0 or  y == 2:
                    if x % 2 == 0:
                        self._grid.append(Piece(x, y, Player.black))
                if y == 1:
                    if (x+1) % 2 == 0:
                        self._grid.append(Piece(x, y, Player.black))

                if y == 5 or y == 7:
                    if (x+1) % 2 == 0:
                        self._grid.append(Piece(x, y, Player.white))
                if y == 6:
                    if x % 2 == 0:
                        self._grid.append(Piece(x, y, Player.white))

    def movePiece(piece, row, col):
        assert self.is_on_grid(row, col)
        assert self.getPieceIdAt(row, col) is None
        self._grid.index(piece)

    def getPieceIdAt(row, col):
        for i, piece in enumerate(self._grid):
            if piece.row = row and piece.col = col:
                return i
        return None

    def __repr__(self):
        out = ''
        
        for y in range(0,8):
            for x in range(0,8):

                if (x+y)%2 == 0:
                    addchr = ' '
                else:
                    addchr = '█'
                
                for p in self._grid:
                    if p.row == x and p.col == y and p.color == Player.white:
                        addchr = '●'
                    elif p.row == x and p.col == y and p.color == Player.black:
                        addchr = '○'
                out += addchr    
                
            out += '\n'
        return out

class GameState:
    def __init__(self, board, next_player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        if self.previous_state is None:
            self.previous_states = frozenset()
        else:
            self.previous_states = frozenset(
                previous.previous_states |
                {(previous.next_player, previous.board.zobrist_hash())})
        self.last_move = move

    def apply_move(self, move):
        """Return the new GameState after applying the move."""
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, self, move)

    @classmethod
    def new_game(cls, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)

    def is_move_self_capture(self, player, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        new_string = next_board.get_go_string(move.point)
        return new_string.num_liberties == 0

    @property
    def situation(self):
        return (self.next_player, self.board)

    def does_move_violate_ko(self, player, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board.zobrist_hash())
        return next_situation in self.previous_states

    def is_valid_move(self, move):
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        return (
            self.board.get(move.point) is None and
            not self.is_move_self_capture(self.next_player, move) and
            not self.does_move_violate_ko(self.next_player, move))

    def is_over(self):
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass

    def legal_moves(self):
        moves = []
        for row in range(1, self.board.num_rows + 1):
            for col in range(1, self.board.num_cols + 1):
                move = Move.play(Point(row, col))
                if self.is_valid_move(move):
                    moves.append(move)
        # These two moves are always legal.
        moves.append(Move.pass_turn())
        moves.append(Move.resign())

        return moves

    def winner(self):
        if not self.is_over():
            return None
        if self.last_move.is_resign:
            return self.next_player
        game_result = compute_game_result(self)
        return game_result.winner


