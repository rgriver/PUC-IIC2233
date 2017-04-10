from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from game_writer import *


class Actions(QWidget):
    quited = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, game):
        super(Actions, self).__init__()
        self.game = game
        actions_box = QGroupBox('Game Actions')
        country_statistics_box = QGroupBox('Country')
        world_statistics_box = QGroupBox('World')
        other_statistics_box = QGroupBox('Other actions')
        day_button = QPushButton('Pass day')
        see_country_button = QPushButton('Print Country State')
        see_measures_button = QPushButton('Print Country Measures')
        save_button = QPushButton('Save Game')
        quit_button = QPushButton('Quit')
        summary_button = QPushButton('Day Summary')
        global_button = QPushButton('Global Report')
        di_button = QPushButton('Deaths and Infections')
        rates_button = QPushButton('Death and Infection Rates')
        clean_button = QPushButton('Clean Countries')
        infected_button = QPushButton('Infected Countries')
        dead_button = QPushButton('Dead Countries')
        population_button = QPushButton('World Population')
        self.countries_combo = QComboBox()
        for countries in self.game.countries:
            self.countries_combo.addItem(countries.name)
        country_layout = QHBoxLayout()
        country_layout.addWidget(QLabel('Country:'))
        country_layout.addWidget(self.countries_combo)
        main_country_layout = QVBoxLayout()
        main_country_layout.addLayout(country_layout)
        main_country_layout.addWidget(see_country_button)
        main_country_layout.addWidget(see_measures_button)
        country_statistics_box.setLayout(main_country_layout)
        actions_layout = QVBoxLayout()
        actions_layout.addWidget(day_button)
        actions_layout.addWidget(save_button)
        actions_layout.addWidget(quit_button)
        actions_box.setLayout(actions_layout)
        world_layout = QVBoxLayout()
        world_layout.addWidget(population_button)
        world_layout.addWidget(clean_button)
        world_layout.addWidget(infected_button)
        world_layout.addWidget(dead_button)
        world_statistics_box.setLayout(world_layout)
        other_layout = QVBoxLayout()
        other_layout.addWidget(summary_button)
        other_layout.addWidget(di_button)
        other_layout.addWidget(rates_button)
        other_statistics_box.setLayout(other_layout)
        layout = QGridLayout()
        layout.addWidget(actions_box, 0, 0)
        layout.addWidget(country_statistics_box, 0, 1)
        layout.addWidget(world_statistics_box, 1, 0)
        layout.addWidget(other_statistics_box, 1, 1)
        day_button.clicked.connect(self.pass_day)
        quit_button.clicked.connect(self.close)
        save_button.clicked.connect(self.save_game)
        see_country_button.clicked.connect(self.see_country_state)
        see_measures_button.clicked.connect(self.see_country_measures)
        summary_button.clicked.connect(self.generate_summary)
        global_button.clicked.connect(self.generate_global_report)
        di_button.clicked.connect(self.see_deaths_and_infections)
        rates_button.clicked.connect(self.see_death_and_infection_rates)
        clean_button.clicked.connect(self.see_clean_countries)
        infected_button.clicked.connect(self.see_infected_countries)
        dead_button.clicked.connect(self.see_dead_countries)
        population_button.clicked.connect(self.see_population_info)
        self.setLayout(layout)

    def pass_day(self):
        if self.game.won():
            message_box = QMessageBox()
            message_box.setText('Congratulations. You killed everyone! Now you'
                                ' can enjoy your loneliness')
            message_box.exec_()
            self.finished.emit()

        elif self.game.lost():
            message_box = QMessageBox()
            message_box.setText('YOU LOSE. Good day, sir.')
            message_box.exec_()
            self.finished.emit()
        else:
            self.game.play()

    def see_country_state(self):
        self.game.generate_country_state(self.countries_combo.currentText())

    def see_country_measures(self):
        self.game.print_measures(self.countries_combo.currentText())

    def generate_summary(self):
        self.game.generate_summary()

    def generate_global_report(self):
        pass

    def see_deaths_and_infections(self):
        self.game.print_deaths_and_infections()

    def see_death_and_infection_rates(self):
        self.game.print_di_rates()

    def see_clean_countries(self):
        self.game.print_clean_countries()

    def see_infected_countries(self):
        self.game.print_infected_countries()

    def see_dead_countries(self):
        self.game.print_dead_countries()

    def see_population_info(self):
        self.game.print_population_info()

    def save_game(self):
        open('game_data.txt', 'w+')
        message_box = QMessageBox()
        self.game.save_game()
        message_box.setText('Game saved')
        message_box.exec_()

    def closeEvent(self, QCloseEvent):
        message_box = QMessageBox()
        message_box.setText('All unsaved progress will be lost. Are you sure y'
                            'ou want to quit the current game?')
        message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        value = message_box.exec_()
        if value == QMessageBox.Cancel:
            QCloseEvent.ignore()
        else:
            self.quited.emit()

    def update(self):
        self.countries_combo.clear()
        for country in self.game.countries:
            self.countries_combo.addItem(country.name)