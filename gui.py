# import the library
from appJar import gui
from threading import Thread

EXIT_BUTTON = "Exit"
RESTART_BUTTON = "Restart"
START_BUTTON = "Start"




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
            # play the first move
            t2 = Thread(target=self.game.play, args=(self,))
            t2.start()
            self.app.openFrame("f2")
            self.app.removeWidget(gui.BUTTON, START_BUTTON)
            self.app.addButton(RESTART_BUTTON, self.press, row=0, column=0)
            self.app.stopFrame()

        elif button == RESTART_BUTTON:
            thread = Thread(target=self.reset, args=())
            thread.start()
        elif self.game.num_empty != self.game.num_cols * self.game.num_rows and self.waiting == 0:
            col = int(button[1])
            thread = Thread(target=self.game.play, args=(self, col,))
            thread.start()

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
        self.app = gui("Connect Four", "600x550")
        #app.setBg("orange")
        self.app.setExpand("both")
        self.app.setPadding([10, 10])

        self.app.startFrame("f0")
        self.app.setSticky("")
        self.app.addRadioButton("diff", "Easy", 0, 1)
        self.app.addRadioButton("diff", "Normal", 0, 2)
        self.app.addRadioButton("diff", "Hard", 0, 3)
        self.app.addButton("Set", self.press, 0, 4)
        self.app.stopFrame()

        self.app.startFrame("f1")
        # grid layout
        self.app.setSticky("news")
        self.app.setExpand("both")
        self.app.setFont(20)

        for row in range(self.game.num_rows):
            for col in range(self.game.num_cols):
                self.app.addNamedButton(" ", str(row) + str(col), self.press, row, col)

        self.app.stopFrame()

        self.app.startFrame("f2")
        self.app.setSticky("")
        # link the buttons to the function called press
        self.app.addButton(START_BUTTON, self.press, row=0, column=0)
        #self.app.addButton(RESTART_BUTTON, self.press, row=0, column=1)
        self.app.addButton(EXIT_BUTTON, self.press, row=0, column=1)
        self.app.stopFrame()

        # start the GUI
        self.app.go()
        # program will not reach the following line unless the windows closes

if __name__ == "__main__":
    from connect_four import *
    connect4 = play_connect4_gui()

