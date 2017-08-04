# import the library
from appJar import gui

EXIT_BUTTON = "Exit"
RESTART_BUTTON = "Restart"


class GUI:
    def __init__(self):
        self.app = None
        self.game = None

    # handle button events
    def press(self, button):
        if button == EXIT_BUTTON:
            self.app.stop()
        elif button == RESTART_BUTTON:
            self.game.reset()
            self.game.play(self)
            self.update()
        else:
            row = int(button[0])
            col = int(button[1])
            self.game.play(self, col)

    def update(self):
        for row in range(self.game.num_rows):
            for col in range(self.game.num_cols):
                self.app.setButton(str(row) + str(col), self.game.board[row][col])

    def init_window(self, game):
        self.game = game
        # create a GUI variable called app
        self.app = gui("Connect Four", "600x550")
        #app.setBg("orange")

        # grid layout
        self.app.setSticky("news")
        self.app.setExpand("both")
        self.app.setFont(20)

        for row in range(self.game.num_rows):
            for col in range(self.game.num_cols):
                self.app.addNamedButton(" ", str(row) + str(col), self.press, row, col)

        # link the buttons to the function called press
        self.app.addButtons([RESTART_BUTTON, EXIT_BUTTON], self.press, row=self.game.num_rows+1, colspan=self.game.num_cols)

        # start the GUI
        self.app.go()
        # program will not reach the following line unless the windows closes

if __name__ == "__main__":
    from connect_four import *
    connect4 = play_connect4_gui()

