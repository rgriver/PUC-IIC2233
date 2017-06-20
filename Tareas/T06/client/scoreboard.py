from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Scoreboard(QListWidget):
    def __init__(self):
        super(Scoreboard, self).__init__()
        style = "QListWidget {" \
                "background-color: rgb(208, 213, 216);" \
                "border-radius:10px}"
        self.setStyleSheet(style)

    def update_time(self, time_table):
        self.clear()
        for e in time_table:
            text = e[0] + ': ' + str(e[1]) + ' seconds | ' + str(e[2]) + \
                   ' points | ' + str(e[3])
            self.addItem(QListWidgetItem(text))

    def update_scores(self, score_table):
        print('scored updated')
        self.clear()
        for e in score_table:
            text = e[0] + ': ' + str(e[1]) + ' points'
            self.addItem(QListWidgetItem(text))
