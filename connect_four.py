from game_node import *
from gui import *
from threading import Thread
from constants import Constants
import copy


class ConnectFour:

    def __init__(self, mode, p1=Constants.PLAYER_1_NAME, p2=Constants.PLAYER_2_NAME, difficulty=Constants.EASY, difficulty2=Constants.EASY, num_rows=Constants.NUM_ROWS, num_cols=Constants.NUM_COLS, gui=False, board=None):
        """
        initialize a ConnectFour game.

        :param mode: 0 if two player, 1 if player vs AI, 2 if AI vs AI, 3 if gui single
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
        self.difficulty2 = difficulty2
        self.num_empty = None
        self.board = board
        self.curr_turn = self.p1 #for GUI only
        self.first_round_gui = 0
        self.order = [p1, p2]
        self.is_running = 0

        if not board:
            self.reset()
        if mode == 0:
            self.play = self.dual_play
            self.p2 = p2
        elif mode == 1:
            self.play = self.single_player
            self.p2 = Constants.COMPUTER_NAME
        elif mode == 2:
            self.play = self.dual_ai
            self.p1 = Constants.AI_1_NAME
            self.p2 = Constants.AI_2_NAME
        elif mode == 3:
            self.play = self.single_player_gui
            self.p2 = Constants.COMPUTER_NAME
        elif mode == 4:
            self.play = self.dual_ai_gui
            self.p1 = Constants.AI_1_NAME
            self.p2 = Constants.AI_2_NAME

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
        self.board = [[Constants.EMPTY_SLOT] * self.num_cols for i in range(self.num_rows)]
        self.num_empty = self.num_cols * self.num_rows
        self.first_round_gui = 1

    def get_copy(self):
        return copy.deepcopy(self)

    def change_mode(self, mode):
        """
        :param mode: int representation of game mode
        :return: None
        """
        self.mode = mode
        if mode == 0:
            self.play = self.dual_play
            self.p2 = p2
        elif mode == 1:
            self.play = self.single_player
            self.p2 = Constants.COMPUTER_NAME
        elif mode == 2:
            self.play = self.dual_ai
            self.p1 = Constants.AI_1_NAME
            self.p2 = Constants.AI_2_NAME
        elif mode == 3:
            self.play = self.single_player_gui
            self.p2 = Constants.COMPUTER_NAME
        elif mode == 4:
            self.play = self.dual_ai_gui
            self.p1 = Constants.AI_1_NAME
            self.p2 = Constants.AI_2_NAME

    def next_move(self, round, move):
        """
        Set next move and update board

        :param round: current player
        :param move: int representation of col num
        :return: None

        """
        if round == self.p1:
            token = Constants.TOKEN_1
        elif round == self.p2:
            token = Constants.TOKEN_2
        else:
            raise Exception("No other player exception")
        if move < 0 or move > self.num_cols:
            raise Exception("Error column chosen")
        if self.check_column_full(move):
            raise Exception("column full")
        pos = -1
        while pos < self.num_rows - 1:
            if self.board[pos + 1][move] != Constants.EMPTY_SLOT:
                break
            pos += 1
        self.board[pos][move] = token
        self.num_empty -= 1

    def check_column_full(self, move):
        return self.board[0][move] != Constants.EMPTY_SLOT

    def winning_check(self):
        """
        if tie: return 3
        if game still valid: return 4
        otherwise: return win player
        """
        if self.num_empty == 0:
            # tie
            return "3"
        for token in [Constants.TOKEN_1, Constants.TOKEN_2]:
            for direction in ["vertical", "horizontal", "LD", "RD"]:
                if self.line_check(token, direction):
                    return token
        # game still valid
        return "4"

    def _helper_check_valid(self, row, col):
        """
        check if any empty slot under input slot
        :return: false if has space
        """
        for i in range(row+1, self.num_rows):
            return self.board[i][col] != Constants.EMPTY_SLOT
        return True


    def line_check(self, token, direction, num=4):
        # vertical
        if direction == "vertical":
            for i in range(0, self.num_rows):
                for j in range(0, self.num_cols - 3):
                    test_str = self.board[i][j:j+4]
                    if test_str.count(token) == num and test_str.count(Constants.EMPTY_SLOT) == 4 - num:
                        for index in range(len(test_str)):
                            if test_str[index] == Constants.EMPTY_SLOT and num != 4 and not self._helper_check_valid(i, j + index):
                                return False
                        return True
        # horizontal
        if direction == "horizontal":
            for j in range(0, self.num_cols):
                for i in range(0, self.num_rows - 3):
                    test_str = [self.board[k][j] for k in range(i, i+4)]
                    if test_str.count(token) == num and test_str.count(Constants.EMPTY_SLOT) == 4 - num:
                        return True
        # top right to bottom left
        if direction == "LD":
            for i in range(3, self.num_rows):
                for j in range(3, self.num_cols):
                    test_str = [self.board[i - k][j - k] for k in range(4)]
                    if test_str.count(token) == num and test_str.count(Constants.EMPTY_SLOT) == 4 - num:
                        for index in range(len(test_str)):
                            if test_str[index] == Constants.EMPTY_SLOT and num != 4 and not self._helper_check_valid(i - index, j - index):
                                return False
                        return True
        # top left to bottom right
        if direction == "RD":
            for i in range(3, self.num_rows):
                for j in range(0, self.num_cols - 3):
                    test_str = [self.board[i - k][j + k] for k in range(4)]
                    if test_str.count(token) == num and test_str.count(Constants.EMPTY_SLOT) == 4 - num:
                        for index in range(len(test_str)):
                            if test_str[index] == Constants.EMPTY_SLOT and num != 4 and not self._helper_check_valid(i - index, j + index):
                                return False
                        return True
        return False

    def print_game_status(self):
        """
        print current game board in console
        :return: None
        """
        for i in range(self.num_rows):
            print("    ", end="")
            for j in range(self.num_cols):
                print("| " + str(self.board[i][j]), end=" ")
            print("|")
        num_str = "   "
        for i in range(1, self.num_cols + 1):
            num_str += "   " + str(i)
        print(num_str)

    def random_start(self):
        """
        randomize whoever start the game first
        :return: player list
        """
        player_lst = [self.p1, self.p2]
        random.shuffle(player_lst)
        return player_lst

    def single_player(self):
        """
        Single player game mode
        """
        count = 0
        while True:
            for player in self.order:
                # player 1: Human
                if player == self.p1:
                    print("It is " + player + "'s turn")
                    if count == 0:
                        self.print_game_status()
                    col = self._get_input()
                    self.next_move(player, col)
                # player 2: AI
                elif player == self.p2:
                    count += 1
                    print("It is " + player + "'s turn")
                    col = find_next_move(self, player, self.difficulty)
                    self.next_move(player, col)
                    self.print_game_status()
                # Winning check
                check = self.winning_check()
                if check != "4":
                    self.print_game_status()
                if check == Constants.TOKEN_1:
                    print(self.p1 + " win")
                    return 0
                elif check == Constants.TOKEN_2:
                    print(self.p2 + " win")
                    return 0
                elif check == "3":
                    print("It's a tie")
                    return 0

    def dual_play(self):
        """
        Multi-player game mode
        """
        while True:
            for player in self.order:
                # player move
                print("It is " + player +"'s turn")
                self.print_game_status()
                col = self._get_input()
                self.next_move(player, col)

                # winning check
                check = self.winning_check()
                if check != "4":
                    self.print_game_status()
                if check == Constants.TOKEN_1:
                    print(self.p1 + " win")
                    self.is_running = 0
                    return 0
                elif check == Constants.TOKEN_2:
                    print(self.p2 + " win")
                    self.is_running = 0
                    return 0
                elif check == "3":
                    print("It's a tie")
                    self.is_running = 0
                    return 0

    def dual_ai(self):
        """
        AI VS AI
        :return: 0
        """
        while True:
            for player in self.order:
                print("It is " + player + "'s turn")
                self.print_game_status()
                if player == self.p1:
                    col = find_next_move(self, player, self.difficulty)
                else:
                    col = find_next_move(self, player, self.difficulty2)
                self.next_move(player, col)
                check = self.winning_check()
                if check != "4":
                    self.print_game_status()
                if check == Constants.TOKEN_1:
                    print(self.p1 + " win")
                    return 0
                elif check == Constants.TOKEN_2:
                    print(self.p2 + " win")
                    return 0
                elif check == "3":
                    print("It's a tie")
                    return 0

    def _get_input(self):
        """
        Get input from console
        """
        while True:
            col = input("please select the column from 1 to " + str(self.num_cols) + ": ")
            if not col.isdigit() or int(col) <= 0 or int(col) > self.num_cols:
                print("invalid input!")
            elif self.board[0][int(col)-1] != Constants.EMPTY_SLOT:
                print("column full!")
            else:
                break
        return int(col) - 1

    def single_player_gui(self, window=None, move=-1):
        """
        single player mode gui setup
        :param window: gui window
        :param move: int
        """
        window.waiting = 1

        print(window.game.order)
        print([window.game.p2, window.game.p1])
        if move == -1 and window.game.order == [window.game.p2, window.game.p1]:
            print("It is " + self.p2 + "'s turn")
            col = find_next_move(self, self.p2, self.difficulty)
            self.next_move(self.p2, col)
            self.print_game_status()
            window.update()
            if self.check_game_over_gui(window) != "continue":
                window.waiting = 0
                return 0
        elif move == -2 and window.game.order == [window.game.p1, window.game.p2]:
            self.print_game_status()
            window.update()
        elif self.check_column_full(move):
            window.app.infoBox("Error", "Column Full!")
        else:
            self.next_move(self.p1, move)
            self.print_game_status()
            window.update()
            if self.check_game_over_gui(window) != "continue":
                window.waiting = 0
                return 0
            col = find_next_move(self, self.p2, self.difficulty)
            self.next_move(self.p2, col)
            self.print_game_status()
            window.update()
            if self.check_game_over_gui(window) != "continue":
                window.waiting = 0
                return 0
        window.waiting = 0
        return 0

    def dual_ai_gui(self, window, curr_player):
        """
        AI VS AI mode gui setup
        :param window: gui window
        :param curr_player: str representation of current player
        """
        window.waiting = 1
        # set difficulties
        if curr_player == self.p1:
            difficulty = self.difficulty
        else:
            difficulty = self.difficulty2
        # find moves
        col = find_next_move(self, curr_player, difficulty)
        self.next_move(curr_player, col)
        self.print_game_status()
        # update gui window
        window.update()
        if self.check_game_over_gui(window) != "continue":
            window.waiting = 0
            return 0
        window.waiting = 0
        return 0

    def check_game_over_gui(self, window):
        """
        check whther game still valid
        :param window: gui window
        :return: str representing game status
        """
        check = self.winning_check()
        if check == Constants.TOKEN_1:
            print(self.p1 + " win")
            self.is_running = 0
            if self.mode == 3:
                window.app.infoBox("Game Over", "You win!")
            else:
                window.app.infoBox("Game Over", "AI 1 win!")
            return self.p1
        elif check == Constants.TOKEN_2:
            print(self.p2 + " win")
            self.is_running = 0
            if self.mode == 3:
                window.app.infoBox("Game Over", "You Lose!")
            else:
                window.app.infoBox("Game Over", "AI 2 win!")
            return self.p2
        elif check == "3":
            print("It's a tie")
            self.is_running = 0
            window.app.infoBox("Game Over", "It's a tie!")
            return "tie"
        return "continue"

def play_connect4():
    """
    play connect4 in console
    """
    game = None
    game_type = None
    mode = None
    player1 = None
    player2 = None
    difficulty = None
    difficulty2 = None
    order = None

    print("Welcome to Connect4")
    print ("Please select a game mode:")
    while not game_type:
        game_type = str(input("Type 'Single' or 'Double' or 'AI': "))
        if game_type.lower() == "single":
            mode = 1
            while player1 == None:
                player1 = str(input("Enter player's name:"))
                player2 = "Computer"
            while difficulty == None:
                difficulty = int(input("Enter game difficulty 1 or 2 or 3:"))
            game = ConnectFour(mode, player1, difficulty=difficulty)

        elif game_type.lower() == "double":
            mode = 0
            while player1 == None:
                player1 = str(input("Enter player1's name:"))
            while player2 == None:
                player2 = str(input("Enter player2's name:"))
            game = ConnectFour(mode, player1, player2)
        elif game_type.lower() == "ai":
            mode = 2
            player1 = "SIRI"
            player2 = "CORTANA"
            while difficulty == None:
                difficulty = int(input("Enter game difficulty 1 or 2 or 3 for AI1 {}:".format(player1)))
            while difficulty2 == None:
                difficulty2 = int(input("Enter game difficulty 1 or 2 or 3 for AI2 {}:".format(player2)))
            game = ConnectFour(mode, difficulty=difficulty, difficulty2=difficulty2)
        else:
            game_type = None
    while not order:
        order_str = str(input("Which player first? ({} or {})?".format(player1, player2)))
        if order_str == player1:
            order = True
            game.order = [game.p1, game.p2]
        elif order_str == player2:
            order = True
            game.order = [game.p2, game.p1]
    print("Game initialized, good luck!")
    game.play()
    while True:
        play_again = str(input("Would you like to play again? Enter 'yes' or 'no' "))
        if play_again.lower() == 'y' or play_again.lower() == 'yes':
            play_connect4()
            break
        elif play_again.lower() == 'n' or play_again.lower() == 'no':
            print("Thanks for playing!")
            break
        else:
            print("I don't understand... ")

def play_connect4_gui():
    """
    play connect4 via gui
    :return:
    """
    game = ConnectFour(mode=3, p1="player name", difficulty=4)
    window = GUI(game)
    window.init_window()
    print("thread finished...exiting")


if __name__ == "__main__":
    connect4 = play_connect4()


