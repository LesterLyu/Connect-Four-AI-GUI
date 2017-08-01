from connect_four import *


class GameNode(object):
    def __init__(self, game, player):
        # make sure you do not modify the game instance directly.
        self.game = game
        self.player = player
        self.best_move = None


def heuristic(game, max_player):
    value = 0
    min_player = game.p1 if max_player == game.p2 else game.p2
    tokens = {game.p1: TOKEN_1, game.p2: TOKEN_2}
    # check players
    for direction in ["vertical", "horizontal", "LD", "RD"]:
        for num in range(2, 5):
            if game.line_check(tokens[max_player], direction, num):
                if num == 4:
                    value += float("inf")
                value += num
            if game.line_check(tokens[min_player], direction, num):
                if num == 4:
                    value += float("-inf")
                value -= num
    return value


def extend(node):
    """
    Extend the game, return a list of games that applied all possible moves

    :param game: ConnectFour
    :return: list of game [(GameNode, move), (GameNode, move),...]
    """
    res = []
    for col in range(NUM_COLS):
        new_game = node.game.get_copy()
        try:
            new_game.next_move(COMPUTER_NAME, col)
        except:
            pass
        next_player = node.game.p1 if node.player == node.game.p2 else node.game.p2
        res.append((GameNode(new_game, next_player), col))
    return res


def minimax(node, depth, maximize_player=True):

    if depth == 0 or node.game.winning_check() != "4":  # is terminal
        max_player = node.player if maximize_player else node.game.p1 if node.player == node.game.p2 else node.game.p2
        return heuristic(node.game, max_player)
    # maximizing player
    if maximize_player:
        best_value = float("-inf")
        children = extend(node)
        for child, move in children:
            val = minimax(child, depth - 1, False)
            if best_value < val:
                best_value = val
                node.best_move = move
        return best_value
    # minimizing player
    else:
        best_value = float("inf")
        children = extend(node)
        for child, move in children:
            val = minimax(child, depth - 1, True)
            if best_value > val:
                best_value = val
                node.best_move = move
        node.value = best_value
        return best_value


def find_next_move(game, max_player, depth):
    node = GameNode(game, max_player)
    minimax(node, depth)
    return node.best_move
