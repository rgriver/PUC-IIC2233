import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Menu(QWidget):
    new_game_requested = pyqtSignal()
    saved_game_requested = pyqtSignal()

    def __init__(self):
        super(Menu, self).__init__()
        policy = QSizePolicy()
        policy.setHorizontalStretch(0)
        new_game_button = QPushButton('New Game')
        new_game_button.setSizePolicy(policy)
        load_game_button = QPushButton('Load Game')
        load_game_button.setSizePolicy(policy)
        layout = QVBoxLayout()
        layout.addWidget(QLabel('<p style="text-align: center;"><span style="f'
                                'ont-size:56px;"><span style="color:#ff0000;">'
                                '<strong>Pandemic</strong></span></span></p>'))
        layout.addWidget(new_game_button)
        layout.addWidget(load_game_button)
        layout.setAlignment(new_game_button, Qt.AlignCenter)
        layout.setAlignment(load_game_button, Qt.AlignCenter)
        new_game_button.clicked.connect(self.create_game)
        load_game_button.clicked.connect(self.load_game)
        self.setLayout(layout)

    def create_game(self):
        self.new_game_requested.emit()

    def load_game(self):
        self.saved_game_requested.emit()