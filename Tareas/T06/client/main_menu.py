from client.scoreboard import Scoreboard
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random


class MainMenu(QWidget):
    game_over = pyqtSignal()

    def __init__(self, username, room_names, client, room_view, artists):
        super(MainMenu, self).__init__()
        self.username = QLabel()
        self.pal = QPalette()
        self.pal.setColor(QPalette.Background, QColor(63, 178, 244))
        self.scoreboard = Scoreboard()
        self.room_set = RoomSet(username, room_names, client, room_view, self,
                                artists)
        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet("background-color:transparent;")
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout = QVBoxLayout()
        self.bottom_layout = QHBoxLayout()
        self.layout.addWidget(self.username)
        self.scroll_area.setWidget(self.room_set)
        self.bottom_layout.addWidget(self.scroll_area)
        self.bottom_layout.addWidget(self.scoreboard)
        self.layout.addLayout(self.bottom_layout)
        self.setLayout(self.layout)
        self.setPalette(self.pal)
        self.setFixedWidth(700)

    def set_username(self, username):
        self.username.setText(username)

    def closeEvent(self, event):
        msg_box = QMessageBox()
        msg_box.setText('Are you sure you want to quit?')
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        value = msg_box.exec_()
        if value == QMessageBox.Cancel:
            event.ignore()
        else:
            self.game_over.emit()

    def create_room_buttons(self, param_list):
        self.room_set.add_room_buttons(self.username, param_list[0],
                                       param_list[1])

    def update_scoreboard(self, table):
        self.scoreboard.update_scores(table)


class RoomButton(QPushButton):
    def __init__(self, genre, artist1, artist2):
        super(RoomButton, self).__init__()
        self.setFixedWidth(150)
        self.setFixedHeight(150)
        self.genre = QLabel(genre)
        self.num_players = QLabel('Players in Room: 0')
        self.remaining_time = QLabel('Remaining Time: 0')
        self.artists = QLabel(artist1 + '\n' + artist2)
        layout = QVBoxLayout()
        layout.addWidget(self.genre, alignment=Qt.AlignCenter)
        layout.addWidget(self.num_players)
        layout.addWidget(self.remaining_time)
        layout.addWidget(self.artists)
        self.setLayout(layout)
        style = "QPushButton {" \
                "border-radius:10px;" \
                "background-color: rgb(145, 216, 255);}" \
                "QPushButton:hover {" \
                "background-color: rgb(255, 170, 0);}"
        self.setStyleSheet(style)


class RoomSet(QWidget):
    def __init__(self, username, room_names, client, room_view, menu, artists):
        super(RoomSet, self).__init__()
        self.rooms_layout = QGridLayout()
        self.add_room_buttons(username, room_names, client, room_view, menu,
                              artists)

    def add_room_buttons(self, username, room_names, client, room_view, menu,
                         artists):
        self.rooms_layout = QGridLayout()
        i = j = 0
        copy_artists = list(artists)
        for name, artists in zip(room_names, copy_artists):
            num_iter = 0
            a1 = ''
            a2 = ''
            while True:
                a1 = random.choice(artists)
                a2 = random.choice(artists)
                if a1 != a2 or num_iter > 20:
                    break
                else:
                    num_iter += 1
            button = RoomButton(name, a1, a2)
            button.clicked.connect(
                lambda x=username, y=name: client.enter_room(username, y))
            self.rooms_layout.addWidget(button, i, j)
            button.clicked.connect(room_view.show)
            button.clicked.connect(menu.hide)
            i += j
            if j == 1:
                j = 0
            else:
                j += 1
        self.setLayout(self.rooms_layout)
        self.show()
