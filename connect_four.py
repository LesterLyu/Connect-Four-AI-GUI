from game_puzzle import *

class connectFour(gamePuzzle):

    board = None
    num_rows = None
    num_cols = None
    num_empty = None

    def __init__(self, num_rows=7, num_cols=6):
        if num_rows < 4 or num_cols < 4:
            raise Exception("Too small")
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.reset()

    def reset(self):
        self.board = [["0"] * self.num_cols for i in range(self.num_rows)]
        self.num_empty = self.num_cols * self.num_rows

    def next_move(self, player1, player2, round, move):
        if round == player1:
            token = "1"
        elif round == player2:
            token = "2"
        else:
            raise Exception("No other player exception")

        if move < 0 or move > self.num_cols:
            raise Exception("Error column chosen")

        if self.board[0][move] != "0":
            raise Exception("column full")

        pos = -1
        while pos < self.num_rows - 1:
            if self.board[pos + 1][move] != "0":
                break
            pos += 1
        self.board[pos][move] = token
        self.num_empty -= 1


    def winning_check(self):
        for token in ["1", "2"]:
            for direction in ["vertical", "horizontal", "LD", "RD"]:
                if self._line_check(token, direction):
                    return token

        if self.num_empty == 0:
            return "3" #tie
        return "4" # incomplete

    def _line_check(self, token, direction):
        if direction == "vertical":
            for i in range(0, self.num_rows):
                for j in range(0, self.num_cols - 4):
                    if self.board[i][j:j+4] == 4*[token]:
                        return True

        if direction == "horizontal":
            for j in range(0, self.num_cols):
                for i in range(0, self.num_rows - 4):
                    if self.board[i:i+4][j] == 4*[token]:
                        return True


        if direction == "LD": # top right to bottom left
            for i in range(3, self.num_rows):
                for j in range(0, self.num_cols - 4):
                    if [self.board[i - k][j - k] for k in range(4)] == 4*[token]:
                        return True


        if direction == "RD": # top left to bottom right
            for i in range(0, self.num_rows - 4):
                for j in range(0, self.num_cols - 4):
                    if [self.board[i + k][j + k] for k in range(4)] == 4 * [token]:
                        return True
        return False

    def GTS(self, heur, difficulty):
        pass
        #TODO


    def mini_max(self):
        pass
        #TODO

    def print_puzzle(self):
        for j in range(self.num_cols):
            str = ""
            for i in range(self.num_rows):
                str += self.board[i][j]
            print(str)

    def single_player(self, difficulty):
        #TODO

    def dual_play(self, player1="p1", player2="p2"):
        # while True:
        #     for player in [player1, player2]:
        #         





if __name__ == "__main__":
    connect_four = connectFour()
    player1 = "Jerry"
    player2 = "Lester"
    connect_four.dual_play(player1, player2)


