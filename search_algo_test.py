from connect_four import *
from constants import Constants
from game_node import *
import os

def compare_algo(board1, maxplayer, start_depth=1, limited_depth=7):
    game1 = ConnectFour(1, maxplayer, difficulty=1, board=board1)
    game1.num_empty = 30
    node1 = GameNode(game1, Constants.COMPUTER_NAME)
    node2 = GameNode(game1, Constants.COMPUTER_NAME)

    for i in range(start_depth, limited_depth):
        print("==================depth{}======================".format(i))

        start_time = os.times()[0]
        val = minimax(node1, i, Constants.COMPUTER_NAME, Constants.COMPUTER_NAME)
        time1 = os.times()[0] - start_time
        print("minimax:=", time1, "sec")
        print("minimax for depth", i, "is", val)
        print("minimax best move is: ", node1.best_move)


        start_time2 = os.times()[0]
        val2 = ab_pruning(node2, i, Constants.COMPUTER_NAME, Constants.COMPUTER_NAME)
        time2 = os.times()[0] - start_time2
        print("ab_pruning:=", time2, "sec")
        print("ab_pruning for depth", i, "is", val2)
        print("ab_pruning best move is: ", node2.best_move)
        print("\n")
        print("ab_pruning is {} faster than minimax".format(time1-time2))

        print("==========================================")

if __name__ == "__main__":
    board1 = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', 'X', ' ', ' ', ' '],
              [' ', ' ', ' ', 'O', ' ', ' ', ' '],
              [' ', 'O', 'X', 'O', 'O', ' ', ' '],
              [' ', 'X', 'X', 'O', 'X', ' ', ' '],
              ['X', 'O', 'X', 'X', 'O', 'O', 'O']]
    maxplayer = "Jerry"
    start_depth = 1
    limited_depth = 7
    compare_algo(board1, maxplayer, start_depth, limited_depth)
