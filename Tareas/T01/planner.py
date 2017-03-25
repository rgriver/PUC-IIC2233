from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from time_optimizer import *

class Planner(QWidget):
    def __init__(self, data_collection, user_date):
        super(Planner, self).__init__()
        self.resources = data_collection.get_resources_database()
        self.fires = data_collection.get_fires_database()
        self.forecasts = data_collection.get_forecasts_database()
        self.user_date = user_date
        button = QPushButton('Optimize')
        policy = QSizePolicy()
        policy.setHorizontalStretch(0)
        button.setSizePolicy(policy)
        button.clicked.connect(self.optimize)
        self.id_line = QLineEdit()
        self.id_line.setValidator(QRegExpValidator(QRegExp('^0?|[1-9][0-9]'
                                                           '+$')))
        layout = QVBoxLayout()
        layout.addWidget(QLabel('<b> Strategy Planner</b>'))
        op_layout = QGridLayout()
        op_layout.addWidget(QLabel('Fire ID:'), 0, 0)
        op_layout.addWidget(self.id_line, 0, 1)
        op_layout.addWidget(QLabel('Optimize:'), 1, 0)
        self.option_1 = QRadioButton('Cost')
        self.option_2 = QRadioButton('Resources')
        self.option_3 = QRadioButton('Time')
        self.option_1.setChecked(True)
        op_layout.addWidget(self.option_1, 1, 1)
        op_layout.addWidget(self.option_2, 2, 1)
        op_layout.addWidget(self.option_3, 3, 1)
        op_layout.setSizeConstraint(QLayout.SetFixedSize)
        layout.addLayout(op_layout)
        layout.addWidget(button)
        layout.setAlignment(button, Qt.AlignCenter)
        layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(layout)

    def optimize(self):
        message_box = QMessageBox()
        fire_id = self.id_line.text()
        if self.fires.get_line(fire_id):
            if self.option_1.isChecked():
                message_box.setText('Sorry, but this option is not available'
                                    ' in this version of SuperLuchin.')
            elif self.option_2.isChecked():
                message_box.setText('Sorry, but this option is not available'
                                    ' in this verison of SuperLuchin')
            else:
                self.option_3.setText('Time')
                optimizer = TimeOptimizer(self.fires, self.resources,
                                          self.forecasts, self.user_date,
                                          self.id_line.text())
                optimizer.optimize()
                message_box.setText('Optimization terminated!')
        else:
            message_box.setText('There is no fire registered with that ID')
        message_box.exec_()
