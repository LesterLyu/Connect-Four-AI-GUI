from game_node import *
import copy

EMPTY_SLOT = " "
TOKEN_1 = "X"
TOKEN_2 = "O"
NUM_COLS = 7
NUM_ROWS = 6

# default name
COMPUTER_NAME = "computer"
PLAYER_1_NAME = "p1"
PLAYER_2_NAME = "p2"

# difficulty
MAX_DIFFICULTY = -1
HARD = 20
NORMAL = 10
EASY = 6


class ConnectFour:
    def __init__(self, mode, p1=PLAYER_1_NAME, p2=PLAYER_2_NAME, difficulty=EASY, num_rows=NUM_ROWS, num_cols=NUM_COLS, board=None):
        """
        initialize a ConnectFour game.

        :param mode: 0 if two player, 1 if player vs AI
        :param p1: name of first player
        :param p2: name of second player, not required when mode=1
        :param num_rows: number of rows
        :param num_cols: number of columns
        :param board: for testing
        """
        if num_rows < 4 or num_cols < 4:
            raise Exception("Too small")
        self.mode = mode
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.p1 = p1
        self.difficulty = difficulty
        self.num_empty = None
        self.board = board
        if not board:
            self.reset()
        if mode == 0:
            self.play = self.dual_play
            self.p2 = p2
        else:
            self.play = self.single_player
            self.p2 = COMPUTER_NAME

    def reset(self):
        """
        col1 col2 col3  col4 col5 col6 col7
        [['X', 'X', 'X', 'X', 'X', 'X', 'X'],  row1
        ['X', 'X', 'X', 'X', 'X', 'X', 'X'],   row2
        ['X', 'X', 'X', 'X', 'X', 'X', 'X'],   row3
        ['X', 'X', 'X', 'X', 'X', 'X', 'X'],   row4
        ['X', 'X', 'X', 'X', 'X', 'X', 'X'],   row5
        ['X', 'X', 'X', 'X', 'X', 'X', 'X']]   row6
        """
        self.board = [[EMPTY_SLOT] * self.num_cols for i in range(self.num_rows)]
        self.num_empty = self.num_cols * self.num_rows

    def get_copy(self):
        return copy.deepcopy(self)

    def next_move(self, round, move):
        if round == self.p1:
            token = TOKEN_1
        elif round == self.p2:
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
        if self.num_empty == 0:
            return "3" #tie
        for token in [TOKEN_1, TOKEN_2]:
            for direction in ["vertical", "horizontal", "LD", "RD"]:
                if self.line_check(token, direction):
                    return token
        return "4" # incomplete

    def _helper_check_valid(self, row, col):
        """
        看看棋子的下放是否有空格

        :return: false if has space
        """
        for i in range(row+1, self.num_rows):
            return self.board[i][col] != EMPTY_SLOT
        return True


    def line_check(self, token, direction, num=4):
        if direction == "vertical":
            for i in range(0, self.num_rows):
                for j in range(0, self.num_cols - 3):
                    test_str = self.board[i][j:j+4]
                    #print(test_str, test_str.count(token), test_str.count(EMPTY_SLOT) )
                    if test_str.count(token) == num and test_str.count(EMPTY_SLOT) == 4 - num:
                        for index in range(len(test_str)):
                            if test_str[index] == EMPTY_SLOT and num != 4 and not self._helper_check_valid(i, j + index):
                                #print("not valid")
                                return False
                       # print("valid")
                        return True

        if direction == "horizontal":
            for j in range(0, self.num_cols):
                for i in range(0, self.num_rows - 3):
                    test_str = [self.board[k][j] for k in range(i, i+4)]
                    #print(test_str, test_str.count(token) , test_str.count(EMPTY_SLOT))
                    if test_str.count(token) == num and test_str.count(EMPTY_SLOT) == 4 - num:
                        return True

        if direction == "LD": # top right to bottom left
            for i in range(3, self.num_rows):
                for j in range(3, self.num_cols):
                    test_str = [self.board[i - k][j - k] for k in range(4)]
                    if test_str.count(token) == num and test_str.count(EMPTY_SLOT) == 4 - num:
                        for index in range(len(test_str)):
                            if test_str[index] == EMPTY_SLOT and num != 4 and not self._helper_check_valid(i - index, j - index):
                                return False
                        return True

        if direction == "RD": # top left to bottom right
            for i in range(3, self.num_rows):
                for j in range(0, self.num_cols - 3):
                    test_str = [self.board[i - k][j + k] for k in range(4)]
                    if test_str.count(token) == num and test_str.count(EMPTY_SLOT) == 4 - num:
                        for index in range(len(test_str)):
                            if test_str[index] == EMPTY_SLOT and num != 4 and not self._helper_check_valid(i - index, j + index):
                                return False
                        return True
        return False

    def print_game_status(self):
        for i in range(self.num_rows):
            print("\t", end="")
            for j in range(self.num_cols):
                print("| " + str(self.board[i][j]), end=" ")
            print("|")
        num_str = "   "
        for i in range(1, self.num_cols + 1):
            num_str += "   " + str(i)
        print(num_str)

    def single_player(self):
        while True:
            for player in [self.p1, self.p2]:
                if player == self.p1:
                    print("It is " + player + "'s turn")
                    self.print_game_status()
                    col = self._get_input()
                    self.next_move(player, col)

                elif player == self.p2:
                    col = find_next_move(self, player, self.difficulty)
                    self.next_move(player, col)

                check = self.winning_check()
                if check != "4":
                    self.print_game_status()
                if check == TOKEN_1:
                    print(self.p1 + " win")
                    return 0
                elif check == TOKEN_2:
                    print(self.p2 + " win")
                    return 0
                elif check == "3":
                    print("It's a tie")
                    return 0

    def dual_play(self):
        while True:
            for player in [self.p1, self.p2]:
                print("It is " + player +"'s turn")
                self.print_game_status()
                col = self._get_input()
                self.next_move(player, col)
                check = self.winning_check()
                if check != "4":
                    self.print_game_status()
                if check == TOKEN_1:
                    print(self.p1 + " win")
                    return 0
                elif check == TOKEN_2:
                    print(self.p2 + " win")
                    return 0
                elif check == "3":
                    print("It's a tie")
                    return 0

    def dual_ai(self):
        while True:
            for player in [self.p1, self.p2]:
                print("It is " + player + "'s turn")
                self.print_game_status()
                col = find_next_move(self, player, self.difficulty)
                self.next_move(player, col)
                check = self.winning_check()
                if check != "4":
                    self.print_game_status()
                if check == TOKEN_1:
                    print(self.p1 + " win")
                    return 0
                elif check == TOKEN_2:
                    print(self.p2 + " win")
                    return 0
                elif check == "3":
                    print("It's a tie")
                    return 0


    def _get_input(self):
        while True:
            col = input("please select the column from 1 to " + str(self.num_cols) + ": ")
            if not col.isdigit() or int(col) <= 0 or int(col) > self.num_cols:
                print("invalid input!")
            elif self.board[0][int(col)-1] != EMPTY_SLOT:
                print("column full!")
            else:
                break
        return int(col) - 1

if __name__ == "__main__":


    connect_four2 = ConnectFour(1, "Jerry", difficulty=3)
    #connect_four2.play()
    #connect_four2.single_player()
    connect_four2.dual_ai()

