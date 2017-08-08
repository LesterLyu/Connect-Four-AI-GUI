# import the library
from appJar import gui
from threading import Thread
from constants import *

EXIT_BUTTON = "Exit"
RESTART_BUTTON = "Restart"
START_BUTTON = "Start"

SET_DIFFICULTY_BUTTON = "Set Difficulty"
SET_WHO_FIRST_BUTTON = "Set who first"




class GUI:
    def __init__(self, game):
        self.app = None
        self.game = game
        self.waiting = 1

    # handle button events
    def press(self, button):
        if button == EXIT_BUTTON:
            self.app.stop()
        elif button == START_BUTTON:
            self.game.reset()
            self.update()

            # play the first move
            self.game.is_running = True

            if self.app.getRadioButton("diff") == "Normal":
                print("set normal")
                self.game.difficulty = Constants.NORMAL
            elif self.app.getRadioButton("diff") == "Hard":
                print("set hard")
                self.game.difficulty = Constants.HARD
            else:
                print("set easy")
                self.game.difficulty = Constants.EASY
            if self.app.getRadioButton("who first") == "AI First":
                self.game.order = [self.game.p2, self.game.p1]
                print(self.game.order)
            else:
                self.game.order = [self.game.p1, self.game.p2]
                print(self.game.order)
            self.game.is_running = 1
            if self.game.order == [self.game.p1, self.game.p2]:
                first_round = -2
            else:
                first_round = -1
            t2 = Thread(target=self.game.play, args=(self, first_round))
            t2.start()
            self.app.setButton(START_BUTTON, RESTART_BUTTON)



        # elif button == SET_DIFFICULTY_BUTTON:
        #     print("set difficulty")
        #     self.game.is_running = 0
        #     if self.app.getRadioButton("diff") == "Easy":
        #         print("set easy")
        #         self.game.difficulty = 1
        #     if self.app.getRadioButton("diff") == "Normal":
        #         print("set normal")
        #         self.game.difficulty = 2
        #     if self.app.getRadioButton("diff") == "Hard":
        #         print("set hard")
        #         self.game.difficulty = 4

        elif button == SET_WHO_FIRST_BUTTON:
            print("set order")
            self.game.is_running = 0
            # if self.app.getRadioButton("who first") == "You First":
            #     self.game.order = [self.game.p1, self.game.p2]
            #     print(self.game.order)
            # elif self.app.getRadioButton("who first") == "AI First":
            #     self.game.order = [self.game.p2, self.game.p1]
            #     print(self.game.order)
        elif self.waiting == 0 and self.game.is_running == 1:
            col = int(button[1])
            thread = Thread(target=self.game.play, args=(self, col,))
            thread.start()
        else:
            print(self.game.is_running, self.waiting)

    def reset(self):
        self.waiting = 0
        self.game.reset()
        self.game.play(self)
        self.update()

    def update(self):
        for row in range(self.game.num_rows):
            for col in range(self.game.num_cols):
                self.app.setButton(str(row) + str(col), self.game.board[row][col])

    def init_window(self):
        # create a GUI variable called app
        self.app = gui("Connect Four", "800x550")
        #app.setBg("orange")
        self.app.setExpand("both")
        self.app.setPadding([10, 10])

        self.app.startFrame("f0")
        self.app.setSticky("")
        self.app.addRadioButton("diff", "Easy", 0, 1)
        self.app.addRadioButton("diff", "Normal", 0, 2)
        self.app.addRadioButton("diff", "Hard", 0, 3)
        self.app.addRadioButton("who first", "You First", 1, 1)
        self.app.addRadioButton("who first", "AI First", 1, 2)
        # self.app.addButton("Set Difficulty", self.press, 0, 4)
        # self.app.addButton("Set who first", self.press, 1, 4)
        self.app.stopFrame()

        self.app.startFrame("f1")
        # grid layout
        self.app.setStretch("both")
        self.app.setSticky("news")
        self.app.setFont(20)

        for row in range(self.game.num_rows):
            for col in range(self.game.num_cols):
                self.app.addNamedButton(" ", str(row) + str(col), self.press, row, col)

        self.app.stopFrame()

        self.app.startFrame("f2")
        self.app.setSticky("")
        # link the buttons to the function called press
        self.app.addNamedButton(START_BUTTON, START_BUTTON, self.press, row=0, column=0)
        #self.app.addButton(RESTART_BUTTON, self.press, row=0, column=1)
        self.app.addButton(EXIT_BUTTON, self.press, row=0, column=1)
        self.app.stopFrame()

        # start the GUI
        self.app.go()
        # program will not reach the following line unless the windows closes

if __name__ == "__main__":
    from connect_four import *
    connect4 = play_connect4_gui()

