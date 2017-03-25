from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from resource_state import *


class ResourceEditor(QWidget):
    def __init__(self, fires, resources, date):
        super(ResourceEditor, self).__init__()
        self.resources = resources
        self.fires = fires
        self.date = date
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.resource_state = None
        self.resource_state_text = ''
        self.basic_text = ''
        button = QPushButton('Set Resource')
        most_used_button = QPushButton('Most used resources')
        most_effective_button = QPushButton('Most effective resources')
        policy = QSizePolicy()
        policy.setHorizontalStretch(0)
        button.setSizePolicy(policy)
        most_used_button.setSizePolicy(policy)
        most_effective_button.setSizePolicy(policy)
        button.clicked.connect(self.view_resource)
        self.date.accepted.connect(self.update_text)
        view_group = QGroupBox()
        bottom_group = QGroupBox()
        edit_layout = QHBoxLayout()
        edit_layout.addWidget(QLabel('Resource ID:'))
        self.id_line = QLineEdit()
        self.id_line.setValidator(QRegExpValidator(QRegExp('^0?|[1-9]+'
                                                           '[0-9]+$')))
        edit_layout.addWidget(self.id_line)
        view_layout = QVBoxLayout()
        view_layout.addLayout(edit_layout)
        view_layout.addWidget(button)
        view_layout.setAlignment(button, Qt.AlignLeft)
        view_layout.addWidget(self.text)
        bottom_layout = QVBoxLayout()
        bottom_layout.addWidget(most_used_button)
        bottom_layout.addWidget(most_effective_button)
        bottom_layout.setAlignment(most_effective_button, Qt.AlignCenter)
        bottom_layout.setAlignment(most_used_button, Qt.AlignCenter)
        view_group.setLayout(view_layout)
        bottom_group.setLayout(bottom_layout)
        layout = QVBoxLayout()
        layout.addWidget(view_group)
        layout.addWidget(bottom_group)
        self.setLayout(layout)

    def view_resource(self):
        message_box = QMessageBox()
        if self.id_line.text() == '':
            message_box.setText('Please fill out all the fields')
            message_box.exec_()
        else:
            line = self.resources.get_line(self.id_line.text())
            if line:
                self.resource_state = ResourceState(self.date, self.resources,
                                               self.fires, self.id_line.text())
                self.resource_state.update_state()
                info_str = ''
                item_names = [
                    'ID: ',
                    'Tipo: ',
                    'Latitud: ',
                    'Longitud: ',
                    'Velocidad: ',
                    'Autonomía: ',
                    'Delay: ',
                    'Tasa de extinción: ',
                    'Costo: '
                ]
                for item, name in zip(line, item_names):
                    word = name + item + '\n'
                    info_str += word
                self.basic_text = info_str
                self.resource_state_text = self.resource_state.\
                    get_state_string()
                self.text.setText(self.basic_text + self.resource_state_text)
            else:
                message_box.setText('There is no resource registered with '
                                    'that ID')
                message_box.exec_()

    def update_text(self):
        if self.resource_state is not None:
            self.resource_state.update_state()
            self.resource_state_text = self.resource_state.get_state_string()
            self.text.setText(self.basic_text + self.resource_state_text)