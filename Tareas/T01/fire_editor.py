from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
from date_time import *
from user_date import *


class FireEditor(QWidget):
    def __init__(self, fires, user_date):
        super(FireEditor, self).__init__()
        add_layout = QGridLayout()
        add_button = QPushButton('Add Fire')
        policy = QSizePolicy()
        policy.setHorizontalStretch(0)
        add_button.setSizePolicy(policy)
        view_active_button = QPushButton('View Active Fires')
        view_ext_button = QPushButton('View Extinguished Fires')
        add_box = QGroupBox()
        view_box = QGroupBox()
        self.fires = fires
        self.user_date = user_date
        self.lat_line = QLineEdit()
        self.lat_line.setValidator(QRegExpValidator(QRegExp('^-?(0?|[1-9][0-9]'
                                                            '+)?(\.\d+)?$')))
        self.lon_line = QLineEdit()
        self.lon_line.setValidator(QRegExpValidator(QRegExp('^-?(0?|[1-9][0-9]'
                                                            '+)?(\.\d+)?$')))
        self.power_line = QLineEdit()
        self.power_line.setValidator(QRegExpValidator(QRegExp('0?|[1-9]\d+')))
        self.date_line = QLineEdit()
        self.time = QTimeEdit()
        self.time.setDisplayFormat('HH:mm:ss')
        self.date = QDateEdit()
        self.date.setDisplayFormat('dd-MM-yyyy')
        main_add_layout = QVBoxLayout()
        add_layout.addWidget(QLabel('Latitude:'), 0, 0)
        add_layout.addWidget(self.lat_line, 0, 1)
        add_layout.addWidget(QLabel('Longitude:'), 1, 0)
        add_layout.addWidget(self.lon_line, 1, 1)
        add_layout.addWidget(QLabel('Power:'), 2, 0)
        add_layout.addWidget(self.power_line, 2, 1)
        add_layout.addWidget(QLabel('Date:'), 3, 0)
        add_layout.addWidget(self.date, 3, 1)
        add_layout.addWidget(QLabel('Time:'))
        add_layout.addWidget(self.time)
        main_add_layout.addLayout(add_layout)
        main_add_layout.addWidget(add_button)
        main_add_layout.setAlignment(add_button, Qt.AlignCenter)
        add_box.setLayout(main_add_layout)
        view_layout = QVBoxLayout()
        view_layout.addWidget(QLabel('Fire information will be printed to console'))
        view_layout.addWidget(view_active_button)
        view_layout.addWidget(view_ext_button)
        view_box.setLayout(view_layout)
        layout = QVBoxLayout()
        layout.addWidget(add_box)
        layout.addWidget(view_box)
        add_button.clicked.connect(self.add_fire)
        view_active_button.clicked.connect(self.view_active_fires)
        view_ext_button.clicked.connect(self.view_ex_fires)
        self.setLayout(layout)

    def add_fire(self):
        message_box = QMessageBox()
        lat = self.lat_line.text()
        lon = self.lon_line.text()
        power = self.power_line.text()
        date = self.date.date()
        time = self.time.time()
        year = str(date.year()).zfill(2)
        month = str(date.month()).zfill(2)
        day = str(date.day()).zfill(2)
        hour = str(time.hour()).zfill(2)
        minute = str(time.minute()).zfill(2)
        second = str(time.second()).zfill(2)
        date = '-'.join([year, month, day])
        time = ':'.join([hour, minute, second])
        if lat == '' or lon == '' or power == '':
            message_box.setText('Please fill out all the fields')
        else:
            self.fires.set_fire(lat, lon, power, date + ' ' + time)
            message_box.setText('A new fire has been added to the database!')
        message_box.exec_()

    def view_active_fires(self):
        fx = self.fires.get_data()
        all_fires_list = []
        while True:
            line = next(fx, None)
            if line is None:
                break
            line = line.split(',')
            all_fires_list.append(line[0])
        path = 'Reportes Estrategias de Extinción'
        info_dict = dict()
        if os.path.exists(path):
            for file in os.listdir(path):
                resource_list = []
                file = os.path.join(path, file)
                f = open(file, 'r')
                fire_id = next(f).strip()
                dates = [x.split(',')[3] for x in f]
                if not dates:
                    continue
                fire_end = max(dates)
                f = open(file, 'r')
                next(f)
                points = [float(x.strip().split(',')[6]) for x in f]
                total = sum(points)
                effect = 0
                if self.user_date.get_formatted_date_time() < fire_end:
                    active_str = ''
                    f = open(file, 'r')
                    fire_id = next(f).strip()
                    active_str += 'Fire ID: ' + fire_id + '\n'
                    for line in f:
                        line = line.strip()
                        line = line.split(',')
                        if line[2] < self.user_date.get_formatted_date_time():
                            if line[0] not in resource_list:
                                resource_list.append(line[0])
                            start = DateTime()
                            start.set_formatted_date_time(line[2])
                            end = DateTime()
                            end.set_formatted_date_time(line[3])
                            k = (self.user_date - start) / (end - start)
                            effect += float(line[6]) * k
                    if resource_list:
                        active_str += 'Fire ID: ' + fire_id + '\n'
                        active_str += 'Used resources:\n'
                        for r in resource_list:
                            active_str += r + '\n'
                    else:
                        active_str += 'Fire ID: ' + fire_id + '\n'
                        active_str += '0 resources used.\n'
                    active_str += str((effect / total) * 100) + '% extingui' \
                                                                'shed.\n\n'
                    info_dict[fire_id] = active_str
                else:
                    info_dict[fire_id] = ''
        for i in all_fires_list:
            if i in info_dict.keys():
                print(info_dict[i])
            else:
                print('Fire ID: ' + i + '\n0 resources used.\n0.0% '
                                        'extinguished.\n')

    def view_ex_fires(self):
        path = 'Reportes Estrategias de Extinción'
        info_dict = dict()
        if os.path.exists(path):
            for file in os.listdir(path):
                resource_list = []
                file = os.path.join(path, file)
                f = open(file, 'r')
                fire_id = next(f).strip()
                dates = [x.split(',')[3] for x in f]
                if not dates:
                    continue
                fire_end = max(dates)
                f = open(file, 'r')
                next(f)
                points = [float(x.strip().split(',')[6]) for x in f]
                total = sum(points)
                effect = 0
                if self.user_date.get_formatted_date_time() >= fire_end:
                    active_str = ''
                    fire_line = self.fires.get_line(fire_id)
                    fire_start = fire_line[4]
                    f = open(file, 'r')
                    fire_id = next(f).strip()
                    for line in f:
                        line = line.strip()
                        line = line.split(',')
                        if line[0] not in resource_list:
                            resource_list.append(line[0])
                    if resource_list:
                        active_str += 'Fire ID: ' + fire_id + '\n'
                        active_str += 'Start date: ' + fire_start + '\n'
                        active_str += 'End date: ' + fire_end + '\n'
                        active_str += 'Used resources:\n'
                        for r in resource_list:
                            active_str += r + '\n'
                    info_dict[fire_id] = active_str
        if info_dict:
            for i in info_dict.keys():
                print(info_dict[i])
        else:
            print('All fires are out of control!\n')




