from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from map_window import MapWindow


class View:
    def __init__(self, game):
        super(View, self).__init__()
        self.map_window = MapWindow(game)
        game.set_map_window(self.map_window)
        self.start_menu = StartMenu(game)
        self.champion_selector = ChampionSelector(self.start_menu, game,
                                                  self.map_window)
        self.map_window.game_over.connect(self.show_start_menu)

    def show_start_menu(self):
        self.start_menu.show()


class StartMenu(QDialog):
    def __init__(self, game):
        super(StartMenu, self).__init__()
        self.game = game
        self.champion_selector = None
        self.label = QLabel('<p style="text-align: center;"><span style="f'
                            'ont-size:36px;"><span style="color:#ffa000;">'
                            '<span style="outline-style:inherit;">'
                            '<strong><span style="font-family:georgia,'
                            'times,serif;"><span style="font-variant:small-cap'
                            's;">League of Progra</strong></span></span></p>')
        self.new_game_button = QPushButton('New Game')
        self.new_game_button.setFixedWidth(120)
        self.load_game_button = QPushButton('Load Game')
        self.load_game_button.setFixedWidth(120)
        self.load_game_button.clicked.connect(self.accept)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.new_game_button)
        layout.addWidget(self.load_game_button)
        layout.setAlignment(self.new_game_button, Qt.AlignCenter)
        layout.setAlignment(self.load_game_button, Qt.AlignCenter)
        self.setLayout(layout)
        self.setFixedSize(450, 200)
        self.new_game_button.clicked.connect(self.set_champion)
        self.show()

    def set_champion(self):
        self.champion_selector.show()
        self.accept()

    def request_loading(self):
        self.game.load_game()
        self.accept()

    def set_champion_selector(self, champion_selector):
        self.champion_selector = champion_selector


class ChampionSelector(QDialog):
    def __init__(self, menu, game, map_window):
        super(ChampionSelector, self).__init__()
        self.menu = menu
        menu.set_champion_selector(self)
        self.game = game
        self.map_window = map_window
        label = QLabel('<b>Select Your Champion\n<\b>')
        self.clau_radio = QRadioButton('Clau the Sorceress')
        self.hernan_radio = QRadioButton('Hernan the Destructor')
        self.button = QPushButton('OK')
        self.button.setFixedWidth(100)
        self.clau_radio.setChecked(True)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.clau_radio)
        layout.addWidget(self.hernan_radio)
        layout.addWidget(self.button)
        layout.setAlignment(self.button, Qt.AlignCenter)
        self.setLayout(layout)
        self.setFixedSize(250, 180)
        self.button.clicked.connect(self.request_game_creation)

    def request_game_creation(self):
        if self.clau_radio.isChecked():
            self.game.initialize_game('Clau')
        else:
            self.game.initialize_game('Hernan')
        self.map_window.show()
        self.hide()

    def closeEvent(self, QCloseEvent):
        self.menu.show()
