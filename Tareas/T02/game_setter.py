from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class GameSetter(QDialog):
    def __init__(self, game):
        super(GameSetter, self).__init__()
        self.game = game
        self.text = QLineEdit()
        self.ok_button = QPushButton('OK')
        policy = QSizePolicy()
        policy.setHorizontalStretch(0)
        self.ok_button.setSizePolicy(policy)
        main_layout = QVBoxLayout()
        layout = QGridLayout()
        layout.addWidget(QLabel('Country:'), 0, 0)
        layout.addWidget(self.text, 0, 1)
        self.infections_box = QComboBox()
        self.infections_box.addItem('Bacteria')
        self.infections_box.addItem('Parasite')
        self.infections_box.addItem('Virus')
        layout.addWidget(QLabel('Infection:'), 1, 0)
        layout.addWidget(self.infections_box, 1, 1)
        main_layout.addWidget(QLabel('<b>New Game</b>'))
        main_layout.addLayout(layout)
        main_layout.addWidget(self.ok_button)
        main_layout.setAlignment(self.ok_button, Qt.AlignCenter)
        self.ok_button.clicked.connect(self.set_game)
        self.setLayout(main_layout)

    def set_game(self):
        if self.game.create_new_game(self.infections_box.currentText(), self.text.text()):
            self.accept()
        else:
            message_box = QMessageBox()
            message_box.setText('¡Invalid country!')
            message_box.exec_()

    def closeEvent(self, QCloseEvent):
        QCloseEvent.ignore()