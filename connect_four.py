from game import *

EMPTY_SLOT = " "
TOKEN_1 = "X"
TOKEN_2 = "O"

class connectFour(game):

    board = None
    num_rows = None
    num_cols = None
    num_empty = None

    def __init__(self, num_rows=6, num_cols=7, board = None):
        if num_rows < 4 or num_cols < 4:
            raise Exception("Too small")
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.board = board
        self.reset()

    def reset(self):
        self.board = [[EMPTY_SLOT] * self.num_cols for i in range(self.num_rows)]
        self.num_empty = self.num_cols * self.num_rows

    def get_copy(self):
        return connectFour(self.num_rows, self.num_cols, [self.board[i][:] for i in range(self.num_rows)])


    def next_move(self, player1, player2, round, move):
        if round == player1:
            token = TOKEN_1
        elif round == player2:
            token = TOKEN_2
        else:
            raise Exception("No other player exception")

        if move < 0 or move > self.num_cols:
            raise Exception("Error column chosen")

        if self.board[0][move] != EMPTY_SLOT:
            raise Exception("column full")

        pos = -1
        while pos < self.num_rows - 1:
            if self.board[pos + 1][move] != EMPTY_SLOT:
                break
            pos += 1
        self.board[pos][move] = token
        self.num_empty -= 1


    def winning_check(self):
        for token in [TOKEN_1, TOKEN_2]:
            for direction in ["vertical", "horizontal", "LD", "RD"]:
                if self._line_check(token, direction):
                    return token

        if self.num_empty == 0:
            return "3" #tie
        return "4" # incomplete

    def _line_check(self, token, direction):
        if direction == "vertical":
            for i in range(0, self.num_rows):
                for j in range(0, self.num_cols - 3):
                    if self.board[i][j:j+4] == 4*[token]:
                        return True

        if direction == "horizontal":
            for j in range(0, self.num_cols):
                for i in range(0, self.num_rows - 3):
                    if [self.board[k][j] for k in range(i, i+4)] == 4*[token]:
                        return True


        if direction == "LD": # top right to bottom left
            for i in range(3, self.num_rows):
                for j in range(3, self.num_cols):
                    if [self.board[i - k][j - k] for k in range(4)] == 4*[token]:
                        return True


        if direction == "RD": # top left to bottom right
            for i in range(3, self.num_rows):
                for j in range(0, self.num_cols - 3):
                    if [self.board[i - k][j + k] for k in range(4)] == 4 * [token]:
                        return True
        return False

    def GTS(self, heur, difficulty):
        pass
        #TODO


    def mini_max(self):
        pass
        #TODO

    # def print_game_status(self):
    #     for i in range(self.num_rows):
    #         str = ""
    #         for j in range(self.num_cols):
    #             str += self.board[i][j]
    #         print(str)
    def print_game_status(self):
        for i in range(self.num_rows):
            print("\t", end="")
            for j in range(self.num_cols):
                print("| " + str(self.board[i][j]), end=" ")
            print("|")
        print("\t  0   1   2   3   4   5   6 ")

    def single_player(self,difficulty, player1 = "p1", player2 = "computer"):
        while True:
            for player in [player1, player2]:
                print ("It is " + player + "'s turn")
                self.print_puzzle()
                if player == player1:
                    col = input ("please select the column from 0 to " + str(self.num_cols-1) + ": ")
                    while not col.isdigit() or int(col) < 0 or int(col) >= self.num_cols or self.board[0][int(col)] != EMPTY_SLOT:
                        if not col.isdigit() or int(col) < 0 or int(col) >= self.num_cols:
                            col = input ("invalid input, try again: ")
                        elif self.board[0][int(col)] != EMPTY_SLOT:
                            col = input("column full, try again: ")
                    self.next_move(player1, player2, player, int(col))


                elif player == player2:
                    # TODO
                    if difficulty == "hard":
                        break
                    elif difficulty == "easy":
                        break
                    break


                check = self.winning_check()
                if check != "4":
                    self.print_puzzle()
                if check == TOKEN_1:
                    print(player1 + "win")
                    return 0
                elif check == TOKEN_2:
                    print(player2 + "win")
                elif check == "3":
                    print("It's a tie")
                    return 0

        return 0

    def dual_play(self, player1="p1", player2="p2"):
        while True:
            for player in [player1, player2]:
                print("It is " + player +"'s turn")
                self.print_game_status()
                col = input("please select the column from 0 to "+ str(self.num_cols-1) + ": ")
                while not col.isdigit() or int(col) < 0 or int(col) >= self.num_cols or self.board[0][int(col)] != EMPTY_SLOT:
                    if not col.isdigit() or int(col) < 0 or int(col) >= self.num_cols:
                        col = input("invalid input, try again: ")
                    elif self.board[0][int(col)] != EMPTY_SLOT:
                        col = input("column full, try again: ")
                self.next_move(player1, player2, player, int(col))
                check = self.winning_check()
                if check != "4":
                    self.print_game_status()
                if check == TOKEN_1:
                    print(player1 + " win")
                    return 0
                elif check == TOKEN_2:
                    print(player2 + " win")
                    return 0
                elif check == "3":
                    print("It's a tie")
                    return 0





if __name__ == "__main__":
    connect_four = connectFour(num_cols=7, num_rows=6)
    player1 = "Jerry"
    player2 = "Lester"
    connect_four.dual_play(player1, player2)

