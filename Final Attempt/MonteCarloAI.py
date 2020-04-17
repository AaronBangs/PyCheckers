# +JMJ+
# MonteCarloAI.py
# An agent that used a Monte Carlo Search Tree to play.
# 
# Programmed by Ben Campbell, based off of the book source code.

import math
import random
import copy

from Agent import Agent
from RandomAI import RandomAI
from PyCheckers import Player, Move
from CheckerGame import CheckerGame

def fmt(x):
    if x is Player.black:
        return 'B'
    if x is Player.white:
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


# tag::mcts-node[]
class MCTSNode(object):
    def __init__(self, game_state, color, parent=None, move=None):
        self.game_state = game_state
        self.AgentColor = color
        self.parent = parent
        self.move = move
        self.win_counts = {
            Player.black: 0,
            Player.white: 0,
        }
        self.num_rollouts = 0
        self.children = []
        self.unvisited_moves = Agent.getAllMoves(game_state.board, self.AgentColor)
# end::mcts-node[]

# tag::mcts-add-child[]
    def add_random_child(self):
        index = random.randint(0, len(self.unvisited_moves) - 1)
        new_move = self.unvisited_moves.pop(index)
        new_game_state = self.game_state.getState()
        new_game_state.applyMove(copy.deepcopy(new_move))
        new_game_state.currentPlayer = new_game_state.next_player
        new_node = MCTSNode(new_game_state, self.AgentColor, self, new_move)
        self.children.append(new_node)
        return new_node
# end::mcts-add-child[]

# tag::mcts-record-win[]
    def record_win(self, winner):
        self.win_counts[winner] += 1
        self.num_rollouts += 1
# end::mcts-record-win[]

# tag::mcts-readers[]
    def can_add_child(self):
        return len(self.unvisited_moves) > 0

    def is_terminal(self):
        return self.game_state.isOver

    def winning_frac(self, player):
        return float(self.win_counts[player]) / float(self.num_rollouts)
# end::mcts-readers[]


class MonteCarloAI(Agent):
    def __init__(self, color, num_rounds, temperature):
        Agent.__init__(self, color)
        self.num_rounds = num_rounds
        self.temperature = temperature

# tag::mcts-signature[]
    def selectMove(self, board):
        gameState = CheckerGame(Agent(Player.black), Agent(Player.white))
        if self.color is Player.black:
            gameState.blackPlayer = self
            gameState.currentPlayer = self
        else:
            gameState.whitePlayer = self
            gameState.currentPlayer = gameState.whitePlayer
        
        gameState.board = copy.deepcopy(board)
        root = MCTSNode(gameState, self.color)
# end::mcts-signature[]

# tag::mcts-rounds[]
        for i in range(self.num_rounds):
            node = root
            while (not node.can_add_child()) and (not node.is_terminal()):
                node = self.select_child(node)
            
            # Add a new child node into the tree.
            if node.can_add_child():
                node = node.add_random_child()
            
            # Simulate a random game from this node.
            winner = self.simulate_random_game(node.game_state)
            print("\rsimulated game %d/%d" % (i, self.num_rounds))
            
            # Propagate scores back up the tree.
            while node is not None:
                node.record_win(winner)
                node = node.parent
# end::mcts-rounds[]
        #
        scored_moves = [
            (child.winning_frac(gameState.next_player.color), child.move, child.num_rollouts)
            for child in root.children
        ]
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        for s, m, n in scored_moves[:10]:
            print('%s - %.3f (%d)' % (m, s, n))

# tag::mcts-selection[]
        # Having performed as many MCTS rounds as we have time for, we
        # now pick a move.
        best_move = None
        best_pct = -1.0
        for child in root.children:
            child_pct = child.winning_frac(gameState.next_player.color)
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        print('Select move %s with win pct %.3f' % (best_move, best_pct))
        best_move.piece = board.getPieceAt(best_move.piece.x, best_move.piece.y)
        return best_move
# end::mcts-selection[]

# tag::mcts-uct[]
    def select_child(self, node):
        """Select a child according to the upper confidence bound for
        trees (UCT) metric.
        """
        total_rollouts = sum(child.num_rollouts for child in node.children)
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
# end::mcts-uct[]

    @staticmethod
    def simulate_random_game(game):
        randomGame = game.getState()
        randomGame.blackPlayer = RandomAI(Player.black)
        randomGame.whitePlayer = RandomAI(Player.white)
        if randomGame.currentPlayer.color is Player.black:
            randomGame.currentPlayer = randomGame.blackPlayer
        else:
            randomGame.currentPlayer = randomGame.whitePlayer
        return randomGame.playSilently()

'''
for debugging:
from CheckerGame import CheckerGame
from RandomAI import RandomAI
from PyCheckers import Player
from Human import Human

blackPlayer = Human(Player.black)
whitePlayer = Human(Player.white)

game = CheckerGame(blackPlayer, whitePlayer)
game.playSilently()
print(game.board)

'''