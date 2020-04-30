# +JMJ+
# MonteCarloAI.py
# An agent that used a Monte Carlo Search Tree to play.
# 
# Programmed by Ben Campbell, based off of the book source code.

import math
import random
import copy
import time

from py_checkers.agent import Agent, RandomAI
from py_checkers.game import Player, Move, CheckerGame

def fmt(x):
    if x is Player.black:
        return 'B'
    if x is Player.red:
        return 'W'
    if x.is_pass:
        return 'pass'
    if x.is_resign:
        return 'resign'
    if x is Move:
        return '(x: ' + str(x.to_x) + ', y: ' + str(x.to_y) + ')'
    return ''


def show_tree(node, indent='', max_depth=3):
    if max_depth < 0:
        return
    if node is None:
        return
    if node.parent is None:
        print('%sroot' % indent)
    else:
        player = node.parent.game_state.next_player
        move = node.move
        print('%s%s %s %d %.3f' % (
            indent, fmt(player), fmt(move),
            node.num_rollouts,
            node.winning_frac(player),
        ))
    for child in sorted(node.children, key=lambda n: n.num_rollouts, reverse=True):
        show_tree(child, indent + '  ', max_depth - 1)

class MCTSNode(object):
    def __init__(self, game_state, color, parent=None, move=None):
        self.game_state = game_state
        self.agent_color = color
        self.parent = parent
        self.move = move
        self.win_counts = {
            Player.black: 0,
            Player.red: 0,
        }
        self.num_rollouts = 0
        self.children = []
        self.unvisited_moves = game_state.board.get_all_possible_moves(color)

    def add_random_child(self):
        index = random.randint(0, len(self.unvisited_moves) - 1)
        new_move = self.unvisited_moves.pop(index)
        new_game_state = self.game_state.get_state()
        new_game_state.apply_move(copy.deepcopy(new_move))
        new_game_state.current_player = new_game_state.next_player
        new_node = MCTSNode(new_game_state, self.agent_color, self, new_move)
        self.children.append(new_node)
        return new_node

    def add_child(self, move):
        new_game_state = self.game_state.get_state()
        new_game_state.apply_move(copy.deepcopy(move))
        new_game_state.current_player = new_game_state.next_player
        new_node = MCTSNode(new_game_state, self.agent_color, self, move)
        self.children.append(new_node)
        return new_node

    def record_win(self, winner):
        self.win_counts[winner] += 1
        self.num_rollouts += 1

    def can_add_child(self):
        return len(self.unvisited_moves) > 0

    def is_terminal(self):
        return self.game_state.is_over

    def winning_frac(self, player):
        return float(self.win_counts[player]) / float(self.num_rollouts)

    def __str__(self):
        if len(self.children) == 0:
            return "MCTSNode %s;%s;%d/%d []" % (self.game_state.current_player.color, self.move, self.win_counts[self.agent_color], self.num_rollouts)
        else:
            children = '\n, '.join(str(c) for c in self.children)
            return "MCTSNode %s;%s;%d/%d [\n %s \n]" % (self.game_state.current_player.color, self.move, self.win_counts[self.agent_color], self.num_rollouts, children)

class MonteCarloAI(Agent):
    def __init__(self, color, max_time, temperature):
        Agent.__init__(self, color)
        self.max_time = max_time
        self.temperature = temperature

    def select_move(self, board):
        moves = board.get_all_possible_moves(self.color)
        if len(moves) == 1:
            return moves[0]
        if len(moves) == 0:
            return None

        game_state = CheckerGame(Agent(Player.black), Agent(Player.red))
        if self.color is Player.black:
            game_state.black_player = self
            game_state.current_player = self
        else:
            game_state.red_player = self
            game_state.current_player = game_state.red_player
        
        game_state.board = copy.deepcopy(board)
        root = MCTSNode(game_state, self.color)
        self.perform_rollouts(root)
        move = self.choose_best_move_from_tree(root, game_state)
        move.piece = board.get_piece_at(move.piece.x, move.piece.y)
        return move
        # input("Press a key to continue")
    
    def should_double_jump(self, board, piece):
        return True

    def select_double_jump(self, board, piece):
        '''returns a move after a double jump'''
        game_state = CheckerGame(Agent(Player.black), Agent(Player.red))
        if self.color is Player.black:
            game_state.black_player = self
            game_state.current_player = self
        else:
            game_state.red_player = self
            game_state.current_player = game_state.red_player
        
        game_state.board = copy.deepcopy(board)

        moves = board.get_possible_moves(piece)
        moves = list(filter(lambda m: m.isJump(self), moves))

        if len(moves) == 1:
            return moves[0]

        root = MCTSNode(game_state, self.color)
        for move in moves:
            node = root.add_child(move)
            winner = self.simulate_random_game(node.game_state)
            while node is not None:
                node.record_win(winner)
                node = node.parent
        root.unvisited_moves = []
        self.perform_rollouts(root)
        move = self.choose_best_move_from_tree(root, game_state)
        move.piece = board.get_piece_at(move.piece.x, move.piece.y)
        # input("Press a key to continue")
        return move

    def perform_rollouts(self, root):
        end = int(time.time()) + self.max_time
        i = 0
        print("Calculating for %d seconds..." % self.max_time)
        while time.time() < end:
            i = i + 1
        # for i in range(self.num_rounds):
            node = root
            while (not node.can_add_child()) and (not node.is_terminal()) and (len(node.children) > 0):
                node = self.select_child(node)
            
            # Add a new child node into the tree.
            if node.can_add_child():
                node = node.add_random_child()
            
            # Simulate a random game from this node.
            winner = self.simulate_random_game(node.game_state)
            # print("%d seconds left. %d games simulated." % (end - int(time.time()), i), end="          \r")
            
            # Propagate scores back up the tree.
            while node is not None:
                node.record_win(winner)
                node = node.parent
        print("%d random games simulated" % i)
        
        return root

    def choose_best_move_from_tree(self, root, game_state):
        scored_moves = [
            (child.winning_frac(game_state.next_player.color), child.move, child.num_rollouts)
            for child in root.children
        ]
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        for s, m, n in scored_moves[:10]:
            # print('%s - %.3f (%d)' % (m, s, n))
            pass

        # Having performed as many MCTS rounds as we have time for, we
        # now pick a move.
        best_move = None
        best_pct = -1.0
        for child in root.children:
            child_pct = child.winning_frac(game_state.next_player.color)
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        print('Select move %s with win pct %.3f' % (best_move, best_pct))
        return best_move

    def select_child(self, node):
        """Select a child according to the upper confidence bound for
        trees (UCT) metric.
        """
        total_rollouts = max(sum(child.num_rollouts for child in node.children), 1)
        log_rollouts = math.log(total_rollouts)

        best_score = -1
        best_child = None
        # Loop over each child.
        for child in node.children:
            # Calculate the UCT score.
            win_percentage = child.winning_frac(node.game_state.next_player.color)
            exploration_factor = math.sqrt(log_rollouts / child.num_rollouts)
            uct_score = win_percentage + self.temperature * exploration_factor
            # Check if this is the largest we've seen so far.
            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        return best_child

    @staticmethod
    def simulate_random_game(game):
        random_game = game.get_state()
        random_game.black_player = RandomAI(Player.black)
        random_game.red_player = RandomAI(Player.red)
        if random_game.current_player.color is Player.black:
            random_game.current_player = random_game.black_player
        else:
            random_game.current_player = random_game.red_player
        return random_game.playSilently()
