import sys
from PyQt5.QtWidgets import *
from game import *
from view import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    view = View(game)
    app.exit(app.exec_())
