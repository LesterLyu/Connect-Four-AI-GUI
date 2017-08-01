from connect_four import *


class GameNode(object):
    def __init__(self, game):
        # make sure you do not modify the game instance directly.
        self.game_status = game
        self.extensions = []
        # player 1
        self.min = float("inf")
        # player 2
        self.max = float("-inf")
        self.val = None

    def get_curr_game_status(self):
        raise Exception("No Implemented Exceoption")

    def get_extensions(self):
        return self.extensions[:]


def heuristic():

    pass


def extend(game):
    """
    Extend the game, return a list of all possible moves

    :param game: ConnectFour
    :return: list of game
    """
    res = []
    for col in range(NUM_COLS):
        new_game = game.get_copy()
        try:
            new_game.next_move(COMPUTER_NAME, col)
        except:
            pass
        res.append(new_game)
    return res


def generate_game_tree(game, depth = EASY):
    # return the game node
    head = GameNode(game)
    
    
    return head