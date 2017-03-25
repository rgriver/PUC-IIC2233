from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class Window(QMainWindow):
    def __init__(self):
        super(Menu, self).__init__()
        self.user = None
        self.menu

    def set_menu(self, menu):
        self.menu = menu


