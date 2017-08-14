from connect_four import *


if __name__ == "__main__":
    for d in range(1, 7):
        print("-----------------------------------------------------")
        print("testing depth {} ......".format(d))
        game = ConnectFour(2, difficulty=d, difficulty2=d)
        game.play()
