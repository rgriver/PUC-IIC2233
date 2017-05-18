import sys
import random
import functools

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtTest

class Box(QPushButton):
    def __init__(self):
        super(Box, self).__init__()
        self.num = 0

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()
        upper_layout = QHBoxLayout()
        hide_button = QPushButton('Ocultar')
        hide_button.clicked.connect(self.hide_buttons)
        self.label = QLabel('Intentos: 0')
        self.attempts = 0
        self.num_couples = 0
        self.current_buttons = []
        self.pixmaps = []
        self.check_if_equal = False
        self.request = False
        for k in range(12):
            self.pixmaps.append(QPixmap('Imgs/' + str(k + 1) + '.png'))
        self.pixmaps.append(QPixmap('Imgs/b.png'))
        buttons_to_check = []

        choices = []
        for k in range(12):
            choices.append(k)
            choices.append(k)
        choices.append(12)
        print(choices)


        default_pixmap = QPixmap('Imgs/back.png')
        for i in range(5):
            for j in range(5):
                index = random.choice(choices)
                choices.remove(index)
                pixmap = self.pixmaps[index]
                button = Box()
                icon = QIcon()
                icon.addPixmap(default_pixmap, QIcon.Normal)
                icon.addPixmap(pixmap, QIcon.Disabled)
                button.setIcon(icon)
                button.setFixedHeight(100)
                button.setFixedWidth(100)
                button.setIconSize(QSize(100, 100))
                button.num = index
                grid_layout.addWidget(button, i, j)
                button.clicked.connect(functools.partial(self.change_icon, button))
                button.setEnabled(True)
        upper_layout.addWidget(hide_button)
        upper_layout.addWidget(self.label)
        main_layout.addLayout(upper_layout)
        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)
        self.show()

    def change_icon(self, button):
        if len(self.current_buttons) == 2:
            self.label.setText('Intentos :' + str(self.attempts))
            return 0
        if button.num == 12:
            self.attempts += 10
            self.label.setText('Intentos: ' + str(self.attempts))
            button.setEnabled(False)
            return 0
        button.setEnabled(False)
        self.current_buttons.append(button)
        if self.check_if_equal is False:
            self.check_if_equal = True
        else:
            if self.current_buttons[0].num is self.current_buttons[1].num:
                print('great!')
                self.num_couples += 1
                if self.num_couples == 12:
                    self.hide()
                    msg = QMessageBox()
                    msg.setText('Ganaste!')
                    msg.exec_()
            else:
                self.attempts += 1
                self.label.setText('Intentos :' + str(self.attempts))
                QtTest.QTest.qWait(3000)
                for f in self.current_buttons:
                    f.setEnabled(True)
            self.check_if_equal = False

            self.current_buttons = []

    def hide_buttons(self):
        if len(self.current_buttons) == 2:
            for btn in self.current_buttons:
                btn.setEnabled(True)

    def hide_request(self):
        self.request = True
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    app.exit(app.exec_())
