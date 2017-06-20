from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Login(QDialog):
    request_connection = pyqtSignal(str)
    user_names_requested = pyqtSignal()
    username_validated = pyqtSignal()
    login_closed = pyqtSignal()

    def __init__(self):
        super(Login, self).__init__()
        self._menu = None
        self.champion_selector = None
        self.label = QLabel('<p style="text-align: center;"><span style="f'
                            'ont-size:36px;"><span style="color:#ffa000;">'
                            '<span style="outline-style:inherit;">'
                            '<strong><span style="font-family:Helvetica'
                            'times,serif;"><span style="font-variant:small-cap'
                            's;">PograPop</strong></span></span></p>')
        self.text_line = QLineEdit()
        self.text_line.setPlaceholderText('Username')
        self.new_game_button = QPushButton('Connect')
        self.new_game_button.setFixedWidth(120)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(QLabel('Please enter your username.'))
        layout.addWidget(self.text_line)
        layout.addWidget(self.new_game_button)
        layout.setAlignment(self.new_game_button, Qt.AlignCenter)
        self.setLayout(layout)
        self.setFixedSize(300, 200)
        self.new_game_button.clicked.connect(self.send_names_command)
        self.show()

    def send_names_command(self):
        if self.text_line.text():
            self.user_names_requested.emit()

    def validate_command(self, user_names):
        if self.text_line.text() not in user_names:
            self.username_validated.emit()

    def get_username(self):
        return self.text_line.text()

    def closeEvent(self, event):
        self.login_closed.emit()
