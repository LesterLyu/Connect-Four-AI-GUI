# import the library
from appJar import gui
from threading import Thread
from constants import *


EXIT_BUTTON = "Exit"
EXIT_BUTTON2 = "Exit2"
RESTART_BUTTON = "Restart"
START_BUTTON = "Start"
START_BUTTON2 = "Start2"
NEXT_BUTTON = "Next"


class GUI:
    def __init__(self, game):
        self.app = None
        self.game = game
        self.waiting = 0

    # handle button events
    def press(self, button):
        if button == EXIT_BUTTON or button == EXIT_BUTTON2:
            self.app.stop()
        elif button == START_BUTTON and self.waiting == 0:
            self.game.reset()
            self.update()
            self.game.change_mode(3)
            # play the first move

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

        elif button == START_BUTTON2 and self.waiting == 0:
            print("AI vs AI")
            self.game.reset()
            self.update()
            self.game.change_mode(4)
            self.game.p1 = Constants.AI_1_NAME
            self.game.p2 = Constants.AI_2_NAME
            self.game.curr_turn = self.game.p1


            self.game.is_running = 1
            if self.app.getRadioButton("diff1") == "Normal":
                print("set AI 1 normal")
                self.game.difficulty = Constants.NORMAL
            elif self.app.getRadioButton("diff1") == "Hard":
                print("set AI 1 hard")
                self.game.difficulty = Constants.HARD
            else:
                print("set AI 1 easy")
                self.game.difficulty = Constants.EASY

            if self.app.getRadioButton("diff2") == "Normal":
                print("set AI 2 normal")
                self.game.difficulty2 = Constants.NORMAL
            elif self.app.getRadioButton("diff2") == "Hard":
                print("set AI 2 hard")
                self.game.difficulty2 = Constants.HARD
            else:
                print("set AI 2 easy")
                self.game.difficulty2 = Constants.EASY
            self.app.setButton(START_BUTTON2, RESTART_BUTTON)
            t3 = Thread(target=self.game.play, args=(self, self.game.curr_turn))
            t3.start()
            self.game.curr_turn = self.game.p2


        elif button == NEXT_BUTTON and self.waiting == 0 and self.game.is_running == 1 and self.game.mode == 4:
            t4 = Thread(target=self.game.play, args=(self, self.game.curr_turn,))
            t4.start()
            if self.game.curr_turn == self.game.p1:
                self.game.curr_turn = self.game.p2
            else:
                self.game.curr_turn = self.game.p1

        elif self.waiting == 0 and self.game.is_running == 1 and self.game.mode == 3 and button[-6:] == "Single":
            print("pressed button is " + button[-8:] + " " + str(button[-6:] == "Single"))
            col = int(button[1])
            thread = Thread(target=self.game.play, args=(self, col,))
            thread.start()
        else:
            print(self.game.is_running, self.waiting)

    def reset(self):
        """
        reset game
        """
        self.waiting = 0
        self.game.reset()
        self.game.play(self)
        self.update()

    def update(self):
        """
        Update game board
        """
        for row in range(self.game.num_rows):
            for col in range(self.game.num_cols):
                self.app.setButton(str(row) + str(col) + "Single", self.game.board[row][col])
        for row in range(self.game.num_rows):
            for col in range(self.game.num_cols):
                self.app.setButton(str(row) + str(col) + "AI vs AI", self.game.board[row][col])

    def init_window(self):
        # create a GUI variable called app
        self.app = gui("Connect Four", "800x550")
        self.app.startTabbedFrame("TabbedFrame")

        # First tab setup
        self.app.startTab("Player vs AI")
        self.app.addLabel("l1", "Player vs AI")
        self.app.setExpand("both")
        self.app.setPadding([10, 10])

        #Frame 0: single player mode setups
        self.app.startFrame("f0")
        self.app.setSticky("")
        self.app.addRadioButton("diff", "Easy", 0, 1)
        self.app.addRadioButton("diff", "Normal", 0, 2)
        self.app.addRadioButton("diff", "Hard", 0, 3)
        self.app.addRadioButton("who first", "You First", 1, 1)
        self.app.addRadioButton("who first", "AI First", 1, 2)
        self.app.stopFrame()

        # Frame 1: grid layout
        self.app.startFrame("f1")
        self.app.setStretch("both")
        self.app.setSticky("news")
        self.app.setFont(20)
        for row in range(self.game.num_rows):
            for col in range(self.game.num_cols):
                self.app.addNamedButton(" ", str(row) + str(col) + "Single", self.press, row, col)
        self.app.stopFrame()

        # Frame 2: function buttons
        self.app.startFrame("f2")
        self.app.setSticky("")
        # link the buttons to the function called press
        self.app.addNamedButton(START_BUTTON, START_BUTTON, self.press, row=0, column=0)
        #self.app.addButton(RESTART_BUTTON, self.press, row=0, column=1)
        self.app.addButton(EXIT_BUTTON, self.press, row=0, column=1)
        self.app.stopFrame()

        self.app.stopTab()

        # Second tab setup
        self.app.startTab("AI vs AI")
        self.app.addLabel("l2", "AI vs AI")
        self.app.setExpand("both")
        self.app.setPadding([10, 10])

        # Frame 3: AI vs AI mode setups
        self.app.startFrame("f3")
        self.app.setSticky("")
        self.app.addLabel("AI1", "AI1")
        self.app.addRadioButton("diff1", "Easy", 0, 1)
        self.app.addRadioButton("diff1", "Normal", 0, 2)
        self.app.addRadioButton("diff1", "Hard", 0, 3)
        self.app.addLabel("AI2", "AI2")
        self.app.addRadioButton("diff2", "Easy", 1, 1)
        self.app.addRadioButton("diff2", "Normal", 1, 2)
        self.app.addRadioButton("diff2", "Hard", 1, 3)
        self.app.stopFrame()

        # Frame 4: grid layour
        self.app.startFrame("f4")
        self.app.setStretch("both")
        self.app.setSticky("news")
        self.app.setFont(20)
        for row in range(self.game.num_rows):
            for col in range(self.game.num_cols):
                self.app.addNamedButton(" ", str(row) + str(col) + "AI vs AI", self.press, row, col)
        self.app.stopFrame()

        # Frame 5: function buttons
        self.app.startFrame("f5")
        self.app.setSticky("")
        # link the buttons to the function called press
        self.app.addNamedButton(START_BUTTON, START_BUTTON2, self.press, row=0, column=0)
        self.app.addNamedButton(NEXT_BUTTON, NEXT_BUTTON, self.press, row=0, column=1)
        # self.app.addButton(RESTART_BUTTON, self.press, row=0, column=1)
        self.app.addNamedButton(EXIT_BUTTON, EXIT_BUTTON2, self.press, row=0, column=2)
        self.app.stopFrame()

        self.app.stopTab()
        self.app.stopTabbedFrame()

        # start the GUI
        self.app.go()
        # program will not reach the following line unless the windows closes

if __name__ == "__main__":
    from connect_four import *
    connect4 = play_connect4_gui()

