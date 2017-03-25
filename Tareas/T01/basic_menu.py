from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from resource_state import *
from fire_checker import *


class BasicMenu(QWidget):
    def __init__(self, date, login, database):
        super(BasicMenu, self).__init__()
        self.resources = database.get_resources_database()
        self.fires = database.get_fires_database()
        self.login = login
        self.date = date
        self.basic_info = self.init_resource_info()
        self.resource_state = ResourceState(date, self.resources, self.fires,
                                            self.login.resource_id)
        date_button = QPushButton('Change Date')
        policy = QSizePolicy()
        policy.setHorizontalStretch(0)
        date_button.setSizePolicy(policy)
        resource_box = QGroupBox()
        fires_box = QGroupBox()
        self.fires_text = QTextEdit()
        self.fires_text.setReadOnly(True)
        self.fire_checker = FireChecker(self.fires, self.login)
        self.resource_label = QTextEdit()
        self.resource_label.setReadOnly(True)
        #self.update_resource_state()
        resource_layout = QVBoxLayout()
        resource_layout.addWidget(QLabel('<b>Resource Information</b>'))
        resource_layout.addWidget(self.resource_label)
        fires_layout = QVBoxLayout()
        fires_layout.addWidget(QLabel('<b>Fires</b>'))
        fires_layout.addWidget(self.fires_text)
        layout = QVBoxLayout()
        layout.addLayout(resource_layout)
        layout.addLayout(fires_layout)
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(date_button)
        date_button.clicked.connect(self.date.show)
        self.date.accepted.connect(self.update_resource_state)
        self.date.accepted.connect(self.set_fire_info)
        self.setLayout(main_layout)
        self.show()
        self.setFixedSize(500, 500)

    def update_resource_state(self):
        resource_text = self.basic_info
        self.resource_state.update_state()
        state_str = self.resource_state.get_state_string()
        resource_text += str(state_str)
        self.resource_label.setText(resource_text)

    def init_resource_info(self):
        names = ('ID: ',
                 'Type: ',
                 'Latitude: ',
                 'Longitude: ',
                 'Speed: ',
                 'Maximum working time: ',
                 'Delay: ',
                 'Points: ',
                 'Cost: '
                 )
        basic_info = ''
        resource_id = self.login.resource_id
        for i, j in zip(names, self.resources.get_line(resource_id)):
            basic_info += i + j + '\n'
        return basic_info

    def set_fire_info(self):
        fire_str = self.fire_checker.check()
        self.fires_text.setText(fire_str)



