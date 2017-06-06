from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, \
    QMessageBox


class Store(QWidget):
    def __init__(self, game):
        super(Store, self).__init__()
        self.game = game
        self.hand_weapon_label = QLabel()
        buy_hand_weapon_button = QPushButton('Buy')
        self.distance_weapon_label = QLabel()
        buy_distance_weapon_button = QPushButton('Buy')
        self.boots_label = QLabel()
        buy_boots_button = QPushButton('Buy')
        self.crosier_label = QLabel()
        buy_crosier_weapon_button = QPushButton('Buy')
        self.armor_label = QLabel()
        buy_armor_button = QPushButton('Buy')
        self.card_label = QLabel()
        buy_earth_card_button = QPushButton('Buy')
        layout = QGridLayout()
        layout.addWidget(self.hand_weapon_label, 0, 0)
        layout.addWidget(buy_hand_weapon_button, 0, 1)
        layout.addWidget(self.distance_weapon_label, 1, 0)
        layout.addWidget(buy_distance_weapon_button, 1, 1)
        layout.addWidget(self.boots_label, 2, 0)
        layout.addWidget(buy_boots_button, 2, 1)
        layout.addWidget(self.crosier_label, 3, 0)
        layout.addWidget(buy_crosier_weapon_button, 3, 1)
        layout.addWidget(self.armor_label, 4, 0)
        layout.addWidget(buy_armor_button, 4, 1)
        layout.addWidget(self.card_label, 5, 0)
        layout.addWidget(buy_earth_card_button, 5, 1)
        buy_hand_weapon_button.clicked.connect(self.buy_hand_weapon)
        buy_distance_weapon_button.clicked.connect(self.buy_distance_weapon)
        buy_boots_button.clicked.connect(self.buy_boots)
        buy_crosier_weapon_button.clicked.connect(self.buy_crosier)
        buy_armor_button.clicked.connect(self.buy_armor)
        buy_earth_card_button.clicked.connect(self.buy_card)
        self.setLayout(layout)
        self.hand_weapon_price = 5
        self.hand_weapon_effect = 2
        self.distance_weapon_price = 5
        self.distance_weapon_effect = 2
        self.boots_price = 2
        self.boots_effect = 3
        self.crosier_price = 7
        self.crosier_effect = 2
        self.armor_price = 5
        self.armor_effect = 2
        self.card_price = 10
        self.card_effect = 6
        text = 'Hand Weapon\nPrice: {}\nEffect: {}'.format(
            self.hand_weapon_price, self.hand_weapon_effect)
        self.hand_weapon_label.setText(text)
        text = 'Distance weapon\nPrice: {}\nEffect: {}'.format(
            self.distance_weapon_price, self.distance_weapon_effect)
        self.distance_weapon_label.setText(text)
        text = 'Boots\nPrice: {}\nEffect: {}'.format(
            self.boots_price, self.boots_effect)
        self.boots_label.setText(text)
        text = 'Crosier\nPrice: {}\nEffect: {}'.format(
            self.crosier_price, self.crosier_effect)
        self.crosier_label.setText(text)
        text = 'Armor\nPrice: {}\nEffect: {}'.format(
            self.armor_price, self.armor_effect)
        self.armor_label.setText(text)
        text = 'Earthstone Card\nPrice: {}\nEffect: {}'.format(
            self.card_price, self.card_effect)
        self.card_label.setText(text)

    def init_store(self):
        self.hand_weapon_price = 5
        self.hand_weapon_effect = 2
        self.distance_weapon_price = 5
        self.distance_weapon_effect = 2
        self.boots_price = 2
        self.boots_effect = 3
        self.crosier_price = 7
        self.crosier_effect = 2
        self.armor_price = 5
        self.armor_effect = 2

    def buy_hand_weapon(self):
        if self.check_points(self.hand_weapon_price):
            self.game.points -= self.hand_weapon_price
            self.game.player.damage += self.hand_weapon_effect
            self.hand_weapon_price *= 1.5
            self.hand_weapon_effect *= 1.1
            text = 'Hand Weapon\nPrice: {}\nEffect: {}'.format(
                self.hand_weapon_price, self.hand_weapon_effect)
            self.hand_weapon_label.setText(text)
            msg = QMessageBox()
            msg.setText('New damage: ' + str(self.game.player.damage))
            msg.exec_()

    def buy_distance_weapon(self):
        if self.check_points(self.distance_weapon_price):
            self.game.points -= self.distance_weapon_price
            self.game.player.attack_distance += self.distance_weapon_effect
            self.distance_weapon_price *= 1.5
            self.distance_weapon_effect *= 1.1
            text = 'Distance weapon\nPrice: {}\nEffect: {}'.format(
                self.distance_weapon_price, self.distance_weapon_effect)
            self.distance_weapon_label.setText(text)
            msg = QMessageBox()
            msg.setText('New attack distance: ' +
                        str(self.game.player.attack_distance))
            msg.exec_()

    def buy_boots(self):
        if self.check_points(self.boots_price):
            self.game.points -= self.boots_price
            self.game.player.speed += self.boots_effect
            self.boots_price *= 1.5
            self.boots_effect *= 1.1
            text = 'Boots\nPrice: {}\nEffect: {}'.format(
                self.boots_price, self.boots_effect)
            self.boots_label.setText(text)
            msg = QMessageBox()
            msg.setText('New speed: ' + str(self.game.player.speed))
            msg.exec_()

    def buy_crosier(self):
        if self.check_points(self.crosier_price):
            self.game.points -= self.crosier_price
            self.crosier_price *= 1.5
            self.crosier_effect *= 1.1
            text = 'Crosier\nPrice: {}\nEffect: {}'.format(
                self.crosier_price, self.crosier_effect)
            self.crosier_label.setText(text)

    def buy_armor(self):
        if self.check_points(self.hand_weapon_price):
            self.game.points -= self.hand_weapon_price
            self.armor_price *= 1.5
            self.armor_effect *= 1.1
            text = 'Armor\nPrice: {}\nEffect: {}'.format(
                self.armor_price, self.armor_effect)
            self.armor_label.setText(text)

    def buy_card(self):
        if self.check_points(self.card_price):
            self.game.points -= self.card_price
            self.card_price *= 1.5
            self.card_effect *= 1.1
            text = 'Earthstone Card\nPrice: {}\nEffect: {}'.format(
                self.card_price, self.card_effect)
            self.card_label.setText(text)

    def check_points(self, price):
        if self.game.player is not None:
            if self.game.points >= price:
                return True
            else:
                msg = QMessageBox()
                msg.setText("You don't have enough points to buy this item.")
                msg.exec_()
                return False
