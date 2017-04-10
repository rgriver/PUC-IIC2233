from PyQt5.QtWidgets import *
from menu import *
from game_setter import *
from actions import *

class View:
    def __init__(self, game):
        super(View, self).__init__()
        self.game = game
        self.menu = Menu()
        self.game_setter = GameSetter(game)
        self.actions = Actions(game)
        self.menu.new_game_requested.connect(self.create_new_game)
        self.menu.saved_game_requested.connect(self.load_game)
        self.actions.quited.connect(self.menu.show)
        self.game_setter.accepted.connect(self.actions.update)
        self.game_setter.accepted.connect(self.actions.show)
        self.menu.show()

    def load_game(self):
        message_box = QMessageBox()
        if self.game.load_saved_game():
            message_box.setText('There is no saved data')
            message_box.exec_()
        else:
            self.menu.hide()
            self.actions.show()

    def create_new_game(self):
        self.menu.hide()
        self.game_setter.show()

    def closeEvent(self, QCloseEvent):
        message_box = QMessageBox()
        message_box.setWindowTitle('Exit Pandemic')
        message_box.setText('Do you really want to exit?')
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)