from connect_four import *
from game_node import *
import sys

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) != 3 and len(argv) != 2:
        print("usage: test_helper.py difficulty [-p enable prune]")
        exit(1)

    difficulty = argv[1]  # a number from 1 to 6
    enable_prune = True if argv[2] == "-p" else False  # is alpha-beta prune enabled

    board1 = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', 'X', ' ', ' ', ' '],
              [' ', ' ', ' ', 'O', ' ', ' ', ' '],
              [' ', 'O', 'X', 'O', 'O', ' ', ' '],
              [' ', 'X', 'X', 'O', 'X', ' ', ' '],
              ['X', 'O', 'X', 'X', 'O', 'O', 'O']]
    game1 = ConnectFour(1, "Jerry", difficulty=difficulty, board=board1)
    game1.num_empty = 30  # input any number you want!
    start_time2 = os.times()[0]
    if enable_prune:
        find_next_move(game1, Constants.COMPUTER_NAME, 1)
    else:
        find_next_move(game1, Constants.COMPUTER_NAME, 1, mode="")
    time2 = os.times()[0] - start_time2
    print("takes", time2, "sec to find best move.")

