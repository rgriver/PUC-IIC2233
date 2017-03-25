from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from fire_editor import *
from user_editor import *
from forecast_editor import *
from resource_editor import *
from planner import *
import sys


class AnafMenu(QWidget):
    def __init__(self, login, user_date, data_collection):
        super(AnafMenu, self).__init__()
        self.login = login
        self.date = user_date
        self.users = data_collection.get_users_database()
        self.fires = data_collection.get_fires_database()
        self.forecasts = data_collection.get_forecasts_database()
        self.resources = data_collection.get_resources_database()
        self.user_editor = UserEditor(self.users, self.resources)
        self.fire_editor = FireEditor(self.fires, self.date)
        self.forecast_editor = ForecastEditor(self.forecasts)
        self.resource_editor = ResourceEditor(self.fires, self.resources,
                                              self.date)
        self.planner = Planner(data_collection, user_date)
        # From this point
        stacked_widget = QStackedWidget()
        stacked_widget.addWidget(self.fire_editor)
        stacked_widget.addWidget(self.resource_editor)
        stacked_widget.addWidget(self.user_editor)
        stacked_widget.addWidget(self.forecast_editor)
        stacked_widget.addWidget(self.planner)
        list_widget = QListWidget()
        list_widget.addItem('Fires')
        list_widget.addItem('Resources')
        list_widget.addItem('Users')
        list_widget.addItem('Forecasts')
        list_widget.addItem('Planner')
        button = QPushButton('Change Date')
        size_policy = QSizePolicy()
        size_policy.setVerticalStretch(0)
        button.setSizePolicy(size_policy)
        layout = QHBoxLayout()
        main_layout = QVBoxLayout()
        layout.addWidget(list_widget)
        layout.addWidget(stacked_widget)
        main_layout.addLayout(layout)
        main_layout.addWidget(button)
        self.setLayout(main_layout)
        list_widget.currentRowChanged.connect(stacked_widget.setCurrentIndex)
        button.clicked.connect(self.date.show)

    def set(self):
        self.layout.removeWidget(self.user_editor)
        self.user_editor = UserEditor(self.database)
        self.layout.addWidget(self.user_editor)

    def closeEvent(self, QCloseEvent):
        self.login.signed_in = False
        self.login.show()
