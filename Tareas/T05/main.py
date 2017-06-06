from PyQt5.QtWidgets import QApplication
import sys
from view import View
from game import Game


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    view = View(game)
    app.exec_()

