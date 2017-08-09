import random

from connect_four import *
from constants import Constants
import os


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
def heuristic(game, max_player, curr_player, depth):
    """
    max_player wants to maximize its heuristic
    min_player wants to minimize its heuristic

    :param game:
    :param max_player:
    :return:
    """
    value = 0
    min_player = game.p1 if max_player == game.p2 else game.p2
    tokens = {game.p1: Constants.TOKEN_1, game.p2: Constants.TOKEN_2}
    next_player = game.p1 if curr_player == game.p2 else game.p2
    #print(tokens)
    #print(min_player, max_player)
    #print("max_player=", max_player, " ", tokens[max_player], "curr_player=", curr_player)
    # check players
    for num in range(2, 5):
        #print("===num=", num, "===")
        max_has_num, min_has_num = 0, 0
        for direction in ["vertical", "horizontal", "LD", "RD"]:
            # re-write by Lester
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
    #     print("val=", value)
    # print("val=", value * (depth + 1))
    # game.print_game_status()
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
    next_player = node.game.p1 if curr_player == node.game.p2 else node.game.p2
    if depth == 0 or node.game.winning_check() != "4":  # is terminal
        return heuristic(node.game, max_player, next_player, depth)

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
    #print(move_list)
    for child, move in children:
        move_list.append(move)
        if child.val == best_value:
            best_move_list.append(move)
    # print("minimax move_list:", move_list)
    # print("minimax best_move_list:", best_move_list)
    if len(best_move_list) == 0:
        node.best_move = random.choice(move_list)
    elif len(best_move_list) == 1:
        node.best_move = best_move_list[0]
    else:
        node.best_move = random.choice(best_move_list)
    #print("best_val=", best_value)
    #print(len(move_list))
    return best_value


def ab_pruning(node, depth, curr_player, max_player, alpha=Constants.ALPHA, beta=Constants.BETA):
    next_player = node.game.p1 if curr_player == node.game.p2 else node.game.p2
    if depth == 0 or node.game.winning_check() != "4":  # is terminal
        return heuristic(node.game, max_player, next_player, depth)

    children = extend(node, curr_player)
    new_children = []
    #print("next_player", next_player)
    # maximizing player
    if curr_player == max_player:
        best_value = float("-inf")
        for child, move in children:
            new_children.append((child, move))
            child.val = ab_pruning(child, depth - 1, next_player, max_player, alpha, beta)
            best_value = max(best_value, child.val)
            #print("max_player, best val=", best_value, "move =", move)
            alpha = max(best_value, alpha)
            #print (alpha)
            if beta < alpha:
                #print("break here")
                break
    # minimizing player
    else:
        best_value = float("inf")
        for child, move in children:
            new_children.append((child, move))
            child.val = ab_pruning(child, depth - 1, next_player, max_player, alpha, beta)
            best_value = min(best_value, child.val)
            #print("min_player, best val=", best_value, "move =", move)
            beta = min(best_value, beta)
            if beta < alpha:
                break

    # find the best move

    move_list = []
    best_move_list = []
    for child, move in new_children:
        move_list.append(move)
        if child.val == best_value:
            best_move_list.append(move)
    # print("ab move_list:", move_list)
    # print("ab best_move_list:", best_move_list)
    if len(best_move_list) == 0:
        node.best_move = random.choice(move_list)
    elif len(best_move_list) == 1:
        node.best_move = best_move_list[0]
    else:
        node.best_move = random.choice(best_move_list)
    #print(len(move_list))
    #print("best_move=", node.best_move)
    return best_value


def find_next_move(game, max_player, depth, mode = "ab_prune"):
    node = GameNode(game, max_player)
    if mode == "ab_prune":
    #val = minimax(node, depth, max_player, max_player)
        val = ab_pruning(node,depth,max_player,max_player)
    else:
        val = minimax(node, depth, max_player, max_player)
    #print("best_val=", val)
    return node.best_move

# if __name__ == "__main__":
#     board1 = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
#               [' ', ' ', ' ', ' ', ' ', ' ', ' '],
#               [' ', ' ', ' ', ' ', ' ', ' ', ' '],
#               [' ', ' ', ' ', 'X', 'O', ' ', ' '],
#               ['O', ' ', 'O', 'X', 'X', 'X', ' '],
#               ['O', 'O', 'X', 'X', 'O', 'X', ' ']]
#
#     game = ConnectFour(0, "Jerry", "Lester", board=board1)
#     game.num_empty = 30  # input any number you want!
#     node = GameNode(game, "Jerry")
#
#     board1 = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
#               [' ', ' ', ' ', 'X', ' ', ' ', ' '],
#               [' ', ' ', ' ', 'O', ' ', ' ', ' '],
#               [' ', 'O', 'X', 'O', 'O', ' ', ' '],
#               [' ', 'X', 'X', 'O', 'X', ' ', ' '],
#               ['X', 'O', 'X', 'X', 'O', 'O', 'O']]
#
#     game1 = ConnectFour(1, "Jerry", difficulty=1, board=board1)
#     game1.num_empty = 30
#     node1 = GameNode(game1, Constants.COMPUTER_NAME)
#     node2 = GameNode(game1, Constants.COMPUTER_NAME)
#
#     for i in range(1, 7):
#         print("==================depth{}======================".format(i))
#
#         start_time = os.times()[0]
#         val = minimax(node1, i, Constants.COMPUTER_NAME, Constants.COMPUTER_NAME)
#         time = os.times()[0] - start_time
#         print("minimax:=", time, "sec")
#         print("minimax for depth", i, "is", val)
#         print("minimax best move is: ", node1.best_move )
#
#         # val2 =  ab_pruning(node, 5, "Jerry", "Jerry")
#         start_time2 = os.times()[0]
#         val2 = ab_pruning(node2, i, Constants.COMPUTER_NAME, Constants.COMPUTER_NAME)
#         time2 = os.times()[0] - start_time2
#         print("ab_prunning:=", time2, "sec")
#         print("ab_prunning for depth", i, "is", val2)
#         print("ab_prunning best move is: ", node2.best_move)
#
#         print("==========================================")

