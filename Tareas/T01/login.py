import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Login(QDialog):
    def __init__(self, database):
        super(Login, self).__init__()
        self.signed_in = False
        self.database = database
        self.resource_id = None
        self.setWindowTitle('Sign in to SuperLuchin')
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        label_title = QLabel('<b>Sign In</b>')
        label_name = QLabel('Username')
        label_password = QLabel('Password')
        self.name = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.button = QPushButton('Sign in', self)
        self.button.setFixedWidth(100)
        self.button.clicked.connect(self.validate_credentials)
        layout = QVBoxLayout()
        layout.addWidget(label_title)
        layout.addWidget(label_name)
        layout.addWidget(self.name)
        layout.addWidget(label_password)
        layout.addWidget(self.password)
        layout.addWidget(self.button)
        layout.setAlignment(self.button, Qt.AlignCenter)
        self.setLayout(layout)
        self.setFixedSize(250, 200)
        self.show()

    def validate_credentials(self):
        name = self.name.text()
        password = self.password.text()
        msg_box = QMessageBox()
        if name == '':
            msg_box.setText('Please enter your username')
        elif password == '':
            msg_box.setText('Please enter your password')
        else:
            status = self.database.check_credentials(name, password)
            if status:
                msg_box.setText('Success!')
                self.resource_id = self.database.get_resource_id(name)
                self.password.clear()
                self.name.clear()
                self.accept()
            else:
                msg_box.setText('The credentials you entered cannot be determined to be authentic.')
        msg_box.exec_()

    def sign_out(self):
        self.signed_in = False

    def get_resource_id(self):
        return self.resource_id