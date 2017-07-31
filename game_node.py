from game import *
from connect_four import *

class gameNode(object):

    def __init__(self, game):
        self.game_status = game
        self.extensions = []
        self.min =  99999
        self.max =  -99999
        self.val = None

    def get_curr_game_status(self):
        raise Exception("No Implemented Exceoption")

    def get_extensions(self):
        return self.extensions[:]




def generate_game_tree(game, depth = -1):
    # return the game node
    pass