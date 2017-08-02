import random

from connect_four import *


class GameNode(object):
    def __init__(self, game, player):
        # make sure you do not modify the game instance directly.
        self.game = game
        self.player = player
        self.val = None
        self.best_move = None


# TODO
# has known bugs
# not completed, please complete this first (you can rewrite it)
def heuristic(game, max_player, curr_player):
    """
    max_player wants to maximize its heuristic
    min_player wants to minimize its heuristic

    :param game:
    :param max_player:
    :return:
    """
    value = 0
    min_player = game.p1 if max_player == game.p2 else game.p2
    tokens = {game.p1: TOKEN_1, game.p2: TOKEN_2}
    #print(tokens)
    #print(min_player, max_player)
    print("max_player=", max_player, " ", tokens[max_player], "curr_player=", curr_player)
    # check players
    for direction in ["vertical", "horizontal", "LD", "RD"]:
        for num in range(2, 5):
            # find the grade for max_player
            if game.line_check(tokens[max_player], direction, num):
                # next player is max_player
                if num == 3 and curr_player == min_player:
                    value = max(value, 200)
                    print("val=", value)
                    game.print_game_status()
                    return value
                # next player is min_player
                elif num == 3 and curr_player == max_player:
                    value += 100
                if num == 4:
                    value = max(value, 300)
                value += num
                #print("+++val=", value)
            if game.line_check(tokens[min_player], direction, num):
                if num == 3 and curr_player == max_player:
                    value = min(value, -200)
                    print("val=", value)
                    game.print_game_status()
                    return value
                elif num == 3 and curr_player == min_player:
                    value -= 100
                if num == 4:
                    value = min(value, -300)
                value -= num
                #print("---val=", value)
    print("val=", value)
    game.print_game_status()
    return value


def extend(node, next_player):
    """
    Extend the game, return a list of games that applied all possible moves

    :param game: ConnectFour
    :return: list of game [(GameNode, move), (GameNode, move),...]
    """
    res = []
    for col in range(NUM_COLS):
        new_game = node.game.get_copy()
        try:
            new_game.next_move(next_player, col)
        except Exception as e:
            #print("cannot make next move due to :", e)
            continue
        res.append((GameNode(new_game, next_player), col))
    return res


def minimax(node, depth, curr_player, max_player):
    next_player = node.game.p1 if curr_player == node.game.p2 else node.game.p2
    if depth == 0 or node.game.winning_check() != "4":  # is terminal
        return heuristic(node.game, max_player, next_player)

    children = extend(node, curr_player)
    #print("next_player", next_player)
    # maximizing player
    if curr_player == max_player:
        best_value = float("-inf")
        for child, move in children:
            child.val = minimax(child, depth - 1, next_player, max_player)
            if best_value < child.val:
                best_value = child.val
    # minimizing player
    else:
        best_value = float("inf")
        for child, move in children:
            child.val = minimax(child, depth - 1, next_player, max_player)
            if best_value > child.val:
                best_value = child.val

    # find the best move
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
    print("best_val=", best_value)
    return best_value


def find_next_move(game, max_player, depth):
    node = GameNode(game, max_player)
    val = minimax(node, depth, max_player, max_player)
    #print("best_val=", val)
    return node.best_move
