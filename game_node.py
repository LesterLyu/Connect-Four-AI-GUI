import random
import os
from connect_four import *
from constants import Constants

class GameNode(object):
    def __init__(self, game, player):
        # make sure you do not modify the game instance directly.
        self.game = game
        self.player = player
        self.val = None
        self.best_move = None


def heuristic(game, max_player, curr_player, depth):
    """
    max_player wants to maximize its heuristic
    min_player wants to minimize its heuristic

    :param game: ConnectFour
    :param max_player: current game max player
    :param curr_player:
    :param depth: search depth
    :return: heuristic value
    """
    value = 0
    min_player = game.p1 if max_player == game.p2 else game.p2
    tokens = {game.p1: Constants.TOKEN_1, game.p2: Constants.TOKEN_2}
    next_player = game.p1 if curr_player == game.p2 else game.p2

    # check players
    for num in range(2, 5):
        max_has_num, min_has_num = 0, 0
        for direction in ["vertical", "horizontal", "LD", "RD"]:
            max_has_num += game.line_check(tokens[max_player], direction, num)
            min_has_num += game.line_check(tokens[min_player], direction, num)
        if num == 2:
            if max_has_num > 0:
                value += num * max_has_num
            if min_has_num > 0:
                value -= num * min_has_num
        elif num == 3:
            # max player will win for sure
            if max_has_num > 0 and next_player == max_player:
                value += 200
            # min player will win for sure
            elif min_has_num > 0 and next_player == min_player:
                value -= 200
            # max player may win
            elif max_has_num > 0 and next_player == min_player and not min_has_num > 0:
                value += 50
            # min player may win
            elif min_has_num > 0 and next_player == max_player and not max_has_num > 0:
                value -= 50
            # max player will loss
            elif max_has_num > 0 and min_has_num > 0 and next_player == min_player:
                value -= 200
            # min player will loss
            elif max_has_num > 0 and min_has_num > 0 and next_player == max_player:
                value += 200
        elif num == 4:
            if max_has_num > 0:
                value += 300
            elif min_has_num > 0:
                value += -300
            elif min_has_num > 0 and max_has_num > 0:
                raise Exception("should not reach this")
    return value * (depth + 1)


def extend(node, next_player):
    """
    Extend the game, return a list of games that applied all possible moves

    :param game: ConnectFour
    :return: list of game [(GameNode, move), (GameNode, move),...]
    """
    res = []
    for col in range(Constants.NUM_COLS):
        new_game = node.game.get_copy()
        try:
            new_game.next_move(next_player, col)
        except Exception as e:
            #print("cannot make next move due to :", e)
            continue
        res.append((GameNode(new_game, next_player), col))
    return res


def minimax(node, depth, curr_player, max_player):
    """

    Minimax Searching Algorithm

    :param node: GameNode
    :param depth: serach depth
    :param curr_player: current game player
    :param max_player: current game max player
    :return: heuristic value
    """
    # Terminal state
    next_player = node.game.p1 if curr_player == node.game.p2 else node.game.p2
    if depth == 0 or node.game.winning_check() != "4":  # is terminal
        return heuristic(node.game, max_player, next_player, depth)

    children = extend(node, curr_player)
    # Maximizing player
    if curr_player == max_player:
        best_value = float("-inf")
        for child, move in children:
            child.val = minimax(child, depth - 1, next_player, max_player)
            if best_value < child.val:
                best_value = child.val
    # Minimizing player
    else:
        best_value = float("inf")
        for child, move in children:
            child.val = minimax(child, depth - 1, next_player, max_player)
            if best_value > child.val:
                best_value = child.val

    # Find the best move
    move_list = []
    best_move_list = []
    for child, move in children:
        move_list.append(move)
        if child.val == best_value:
            best_move_list.append(move)
    if len(best_move_list) == 0:
        node.best_move = random.choice(move_list)
    elif len(best_move_list) == 1:
        node.best_move = best_move_list[0]
    else:
        node.best_move = random.choice(best_move_list)
    return best_value


def ab_pruning(node, depth, curr_player, max_player, alpha=Constants.ALPHA, beta=Constants.BETA):
    """

    AlphaBeta Pruning Searching Algorithm

    :param node: GameNode
    :param depth: Search depth
    :param curr_player: current player
    :param max_player: current game max player
    :param alpha: Alpha value
    :param beta: Beta value
    :return:
    """
    # Terminal state
    next_player = node.game.p1 if curr_player == node.game.p2 else node.game.p2
    if depth == 0 or node.game.winning_check() != "4":  # is terminal
        return heuristic(node.game, max_player, next_player, depth)

    children = extend(node, curr_player)
    new_children = []

    # Maximizing player
    if curr_player == max_player:
        best_value = float("-inf")
        for child, move in children:
            new_children.append((child, move))
            child.val = ab_pruning(child, depth - 1, next_player, max_player, alpha, beta)
            best_value = max(best_value, child.val)
            alpha = max(best_value, alpha)
            if beta < alpha:
                break

    # Minimizing player
    else:
        best_value = float("inf")
        for child, move in children:
            new_children.append((child, move))
            child.val = ab_pruning(child, depth - 1, next_player, max_player, alpha, beta)
            best_value = min(best_value, child.val)
            beta = min(best_value, beta)
            if beta < alpha:
                break

    # Find the best move
    move_list = []
    best_move_list = []
    for child, move in new_children:
        move_list.append(move)
        if child.val == best_value:
            best_move_list.append(move)
    if len(best_move_list) == 0:
        node.best_move = random.choice(move_list)
    elif len(best_move_list) == 1:
        node.best_move = best_move_list[0]
    else:
        node.best_move = random.choice(best_move_list)
    return best_value


def find_next_move(game, max_player, depth, mode = "ab_prune"):
    node = GameNode(game, max_player)
    if mode == "ab_prune":
        val = ab_pruning(node,depth,max_player,max_player)
    else:
        val = minimax(node, depth, max_player, max_player)
    return node.best_move
