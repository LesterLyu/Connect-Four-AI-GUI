from game import *
from connect_four import *

MAX_DIFFICALTY = -1
HARD = 20
NORMAL = 10
EASY = 6

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




def generate_game_tree(game, depth = EASY):
    # return the game node
    head = GameNode(game)
    
    
    return head