import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from anaf_menu import *
from basic_menu import *


class Window(QMainWindow):
    def __init__(self, login, date, database):
        super(Window, self).__init__()
        self.login = login
        self.date = date
        self.database = database
        self.setWindowTitle('SuperLuchin')
        self.menu = None
        self.set_menu()

    def set_menu(self):
        resource_id = self.login.get_resource_id()
        if resource_id == '\n' or resource_id == '':
            widget = AnafMenu(self.login, self.date, self.database)
        else:
            widget = BasicMenu(self.date, self.login, self.database)
        self.setCentralWidget(widget)

    def closeEvent(self, QCloseEvent):
        message_box = QMessageBox()
        message_box.setText('Are you sure you want to sign out?')
        message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        value = message_box.exec_()
        if value == QMessageBox.Ok:
            self.login.signed_in = False
            self.login.show()
        else:
            QCloseEvent.ignore()
