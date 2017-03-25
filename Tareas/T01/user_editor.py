import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class UserEditor(QWidget):
    def __init__(self, users, resources):
        super(UserEditor, self).__init__()
        self.users = users
        self.resources = resources
        add_button = QPushButton('Add User')
        policy = QSizePolicy()
        policy.setHorizontalStretch(0)
        add_button.setSizePolicy(policy)
        view_button = QPushButton('View User')
        view_button.setSizePolicy(policy)
        self.id_line = QLineEdit()
        self.id_line.setValidator(QIntValidator(self))
        self.name_line = QLineEdit()
        self.name_line.setValidator(QRegExpValidator(QRegExp('[0-9a-zA-Z]+')))
        self.password_line = QLineEdit()
        self.password_line.setValidator(QRegExpValidator(QRegExp('[0-9a-zA-Z]+')))
        self.resource_id_line = QLineEdit()
        self.resource_id_line.setValidator(QIntValidator(self))
        add_box = QGroupBox()
        view_box = QGroupBox()
        top_layout = QGridLayout()
        top_layout.addWidget(QLabel('Username:'), 0, 0)
        top_layout.addWidget(self.name_line, 0, 1)
        top_layout.addWidget(QLabel('Password:'), 1, 0)
        top_layout.addWidget(self.password_line, 1, 1)
        top_layout.addWidget(QLabel('Resource ID:'), 2, 0)
        top_layout.addWidget(self.resource_id_line, 2, 1)
        main_add_layout = QVBoxLayout()
        main_add_layout.addLayout(top_layout)
        main_add_layout.addWidget(add_button)
        main_add_layout.setAlignment(add_button, Qt.AlignCenter)
        add_box.setLayout(main_add_layout)
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(QLabel('User ID:'))
        bottom_layout.addWidget(self.id_line)
        main_view_layout = QVBoxLayout()
        main_view_layout.addLayout(bottom_layout)
        main_view_layout.addWidget(view_button)
        main_view_layout.setAlignment(view_button, Qt.AlignCenter)
        view_box.setLayout(main_view_layout)
        layout = QVBoxLayout()
        layout.addWidget(add_box)
        layout.addWidget(view_box)
        self.setLayout(layout)
        add_button.clicked.connect(self.add_new_user)
        view_button.clicked.connect(self.view_user)

    def add_new_user(self):
        message_box = QMessageBox()
        name = self.name_line.text()
        password = self.password_line.text()
        resource_id = self.resource_id_line.text()
        if name == '':
            message_box.setText('Please enter a username.')
        elif password == '':
            message_box.setText('Please enter a password.')
        elif not self.resources.get_line(self.resource_id_line.text()) and\
                self.resource_id_line.text() != '':
            message_box.setText('Sorry, but there is no resource registered '
                                'with that ID')
        else:
            success = self.users.add_user(name, password, resource_id)
            message_box.setText('Sorry, but there is already a user with that'
                                ' name.')
            if success:
                message_box.setText('New user added!')
        message_box.exec_()

    def view_user(self):
        message_box = QMessageBox()
        id = self.id_line.text()
        name, password, resource_id = self.users.get_user(id)
        if name == '':
            message_box.setText('Please enter a valid user ID')
            message_box.setIcon(QMessageBox.Warning)
        else:
            info_str = 'Username: ' + name + '\nPassword: ' + password + '\nResource ID: ' + resource_id
            message_box.setText('User Information')
            message_box.setDetailedText(info_str)
        message_box.exec_()
