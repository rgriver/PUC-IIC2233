import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from date_time import *

class UserDate(QDialog, DateTime):
    def __init__(self, login):
        super(UserDate, self).__init__()
        self.login = login
        self.setWindowTitle('Set Date and Time')
        self.date = QDateEdit()
        self.date.setDisplayFormat('dd-MM-yyyy')
        min_date = QDate()
        min_date.setDate(2000, 1, 1)
        self.date.setMinimumDate(min_date)
        self.time = QTimeEdit()
        self.time.setDisplayFormat('HH:mm:ss')
        layout = QGridLayout()
        button = QPushButton('OK')
        button.clicked.connect(self.set_date)
        layout.addWidget(QLabel('<b>Set Date/Time</b>'), 0, 0)
        layout.addWidget(QLabel('Date:'), 1, 0)
        layout.addWidget(self.date, 1, 1)
        layout.addWidget(QLabel('Time:'), 2, 0)
        layout.addWidget(self.time, 2, 1)
        layout.addWidget(button, 3, 1)
        self.setLayout(layout)
        self.setFixedSize(250, 180)

    def set_date(self):
        message_box = QMessageBox()
        self.day = self.date.date().day()
        self.month = self.date.date().month()
        self.year = self.date.date().year()
        self.hour = self.time.time().hour()
        self.minute = self.time.time().minute()
        self.second = self.time.time().second()
        message_box.setText('The date has been updated')
        self.login.signed_in = True
        self.accept()
        message_box.exec_()

    def closeEvent(self, QCloseEvent):
        if not self.login.signed_in:
            message_box = QMessageBox()
            message_box.setText('To continue you must provide a date first. '
                                'Are you sure you want to exit?')
            message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            value = message_box.exec_()
            if value == QMessageBox.Ok:
                self.login.show()
            else:
                QCloseEvent.ignore()
