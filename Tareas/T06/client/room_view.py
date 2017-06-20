from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from client.scoreboard import Scoreboard
from PyQt5.QtMultimedia import QSound


class RoomView(QWidget):
    answer_selected = pyqtSignal(int, int)
    exit_requested = pyqtSignal()
    ready = pyqtSignal()

    def __init__(self):
        super(RoomView, self).__init__()
        self.menu = None
        self.name = None
        self.time_label = QLabel()
        self.time_label.setText('Wait a moment')
        self.pal = QPalette()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.time_label)
        self.pal.setColor(QPalette.Background, QColor(63, 178, 244))
        self.setPalette(self.pal)
        self.choice_a = ChoiceButton()
        self.choice_a.clicked.connect(lambda x: self.select_answer(1))
        self.layout.addWidget(self.choice_a)
        self.choice_b = ChoiceButton()
        self.choice_b.clicked.connect(lambda x: self.select_answer(2))
        self.layout.addWidget(self.choice_b)
        self.choice_c = ChoiceButton()
        self.choice_c.clicked.connect(lambda x: self.select_answer(3))
        self.layout.addWidget(self.choice_c)
        self.choice_d = ChoiceButton()
        self.choice_d.clicked.connect(lambda x: self.select_answer(4))
        self.layout.addWidget(self.choice_d)
        self.scoreboard = Scoreboard()
        self.layout.addWidget(self.scoreboard)
        self.setLayout(self.layout)
        self.timer = QTimer()
        self.timer.timeout.connect(self.increment_time)
        self.playing = False
        self.time = 0
        self.sound = None
        self.filename = None

    def select_answer(self, answer):
        if self.playing:
            self.playing = False
            # self.timer.stop()
            self.time_label.setText('Wait a moment')
            self.answer_selected.emit(answer, self.time)

    def start_playing(self):
        print('start playing')
        self.time = 0
        self.time_label.setText('20')
        self.playing = True
        self.sound = QSound(self.filename)
        self.sound.play()
        self.timer.start(1000)

    def increment_time(self):
        if self.time < 20:
            self.time += 1
            if self.playing:
                self.time_label.setText(str(20 - self.time))
        elif self.time == 20:
            print('stoooooop')
            self.timer.stop()
            self.sound.stop()
            self.ready.emit()
            self.time_label.setText('Wait a moment')
            self.playing = False

    def closeEvent(self, event):
        if self.menu is not None:
            if self.sound is not None:
                self.sound.stop()
            self.timer.stop()
            self.exit_requested.emit()
            self.menu.show()

    def check_answer(self, answered_correctly, time_table):
        msg = QMessageBox()
        if answered_correctly:
            msg.setText('Correct!')
        else:
            msg.setText('Incorrect :(')
        msg.exec_()
        self.scoreboard.update_time(time_table)

    def set_choices(self, a, b, c, d):
        self.choice_a.setText(a)
        self.choice_b.setText(b)
        self.choice_c.setText(c)
        self.choice_d.setText(d)

    def set_filename(self, filename):
        self.filename = filename


class ChoiceButton(QPushButton):
    def __init__(self):
        super(ChoiceButton, self).__init__()
        style = "QPushButton {" \
                "border-radius:10px;" \
                "background-color: rgb(145, 216, 255);}" \
                "QPushButton:hover {" \
                "background-color: rgb(255, 170, 0);}"
        self.setStyleSheet(style)
        self.setFixedHeight(30)
