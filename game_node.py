class gameNode(object):

    def __init__(self, game_puzzle):
        self.puzzle = game_puzzle

    def get_curr_puzzle(self):
        raise Exception("No Implemented Exceoption")

    def get_extensions(self):
        return self.extensions
