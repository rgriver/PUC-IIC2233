from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ForecastEditor(QWidget):
    def __init__(self, forecasts):
        super(ForecastEditor, self).__init__()
        add_layout = QGridLayout()
        add_button = QPushButton('Add Forecast')
        policy = QSizePolicy()
        policy.setHorizontalStretch(0)
        add_button.setSizePolicy(policy)
        add_box = QGroupBox()
        self.forecasts = forecasts
        self.lat_line = QLineEdit()
        self.lat_line.setValidator(QRegExpValidator(QRegExp('^-?(0?|[1-9][0-9]'
                                                            '+)?(\.\d+)?$')))
        self.lon_line = QLineEdit()
        self.lon_line.setValidator(QRegExpValidator(QRegExp('^-?(0?|[1-9][0-9]'
                                                            '+)?(\.\d+)?$')))
        self.radius_line = QLineEdit()
        self.radius_line.setValidator(QRegExpValidator(QRegExp('\d+')))
        self.value_line = QLineEdit()
        self.value_line.setValidator(QRegExpValidator(QRegExp('^(0?|[1-9][0-9]'
                                                              '+)?(\.\d+)?$')))
        self.type = QComboBox()
        self.type.addItem('Clouds')
        self.type.addItem('Rain')
        self.type.addItem('Temperature')
        self.type.addItem('Wind')
        self.start_time = QTimeEdit()
        self.start_time.setDisplayFormat('HH:mm:ss')
        self.start_date = QDateEdit()
        self.start_date.setDisplayFormat('dd-MM-yyyy')
        self.end_time = QTimeEdit()
        self.end_time.setDisplayFormat('HH:mm:ss')
        self.end_date = QDateEdit()
        self.end_date.setDisplayFormat('dd-MM-yyyy')
        main_add_layout = QVBoxLayout()
        add_layout.addWidget(QLabel('Type:'), 0, 0)
        add_layout.addWidget(self.type, 0, 1)
        add_layout.addWidget(QLabel('Latitude:'), 1, 0)
        add_layout.addWidget(self.lat_line, 1, 1)
        add_layout.addWidget(QLabel('Longitude:'), 2, 0)
        add_layout.addWidget(self.lon_line, 2, 1)
        add_layout.addWidget(QLabel('Radius:'), 3, 0)
        add_layout.addWidget(self.radius_line, 3, 1)
        add_layout.addWidget(QLabel('Value:'), 4, 0)
        add_layout.addWidget(self.value_line, 4, 1)
        add_layout.addWidget(QLabel('Start Date:'), 5, 0)
        add_layout.addWidget(self.start_date, 5, 1)
        add_layout.addWidget(QLabel('Start Time:'), 6, 0)
        add_layout.addWidget(self.start_time, 6, 1)
        add_layout.addWidget(QLabel('End Date:'), 7, 0)
        add_layout.addWidget(self.end_date, 7, 1)
        add_layout.addWidget(QLabel('End Time:'), 8, 0)
        add_layout.addWidget(self.end_time, 8, 1)
        main_add_layout.addLayout(add_layout)
        main_add_layout.addWidget(add_button)
        main_add_layout.setAlignment(add_button, Qt.AlignCenter)
        add_box.setLayout(main_add_layout)
        layout = QVBoxLayout()
        layout.addWidget(add_box)
        add_button.clicked.connect(self.add_forecast)
        self.setLayout(layout)

    def add_forecast(self):
        message_box = QMessageBox()
        lat = self.lat_line.text()
        lon = self.lon_line.text()
        radius = self.radius_line.text()
        value = self.value_line.text()
        xstart_time = self.start_time.time()
        xstart_date = self.start_date.date()
        xend_time = self.end_time.time()
        xend_date = self.end_date.date()
        start_year = str(xstart_date.year()).zfill(2)
        start_month = str(xstart_date.month()).zfill(2)
        start_day = str(xstart_date.day()).zfill(2)
        start_hour = str(xstart_time.hour()).zfill(2)
        start_minute= str(xstart_time.minute()).zfill(2)
        start_second = str(xstart_time.second()).zfill(2)
        end_year = str(xend_date.year()).zfill(2)
        end_month = str(xend_date.month()).zfill(2)
        end_day = str(xend_date.day()).zfill(2)
        end_hour = str(xend_time.hour()).zfill(2)
        end_minute = str(xend_time.minute()).zfill(2)
        end_second = str(xend_time.second()).zfill(2)
        start_date = '-'.join([start_year, start_month, start_day])
        start_time = ':'.join([start_hour, start_minute, start_second])
        end_date = '-'.join([end_year, end_month, end_day])
        end_time = ':'.join([end_hour, end_minute, end_second])
        if self.type.currentText() == 'Rain':
            type = 'LLUVIA'
        elif self.type.currentText() == 'Clouds':
            type = 'NUBES'
        elif self.type.currentText() == 'Temperature':
            type = 'TEMPERATURA'
        else:
            type = 'VIENTO'
        if lat == '' or lon == '' or radius == '' or value == '':
            message_box.setText('Please fill out all the fields')
        elif xstart_date > xend_date:
            message_box.setText('End date must be greater than start date')
        elif xstart_date == xend_date and xstart_time >= xend_time:
            message_box.setText('End time must be greater than start time')
        else:
            word = [
                start_date + ' ' + start_time,
                end_date + ' ' + end_time,
                type,
                value,
                lat,
                lon,
                radius
            ]
            word = ','.join(word)
            self.forecasts.add_line(word)

            message_box.setText('A new forecast has been added to the database!')
        message_box.exec_()
