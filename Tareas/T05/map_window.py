from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import math
import numpy
import random
from store import Store


class MapWindow(QGraphicsView):
    game_over = pyqtSignal()
    WIDTH = 1200
    HEIGHT = 650

    def __init__(self, game):
        super(MapWindow, self).__init__()
        self.game = game
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, MapWindow.WIDTH, MapWindow.HEIGHT)
        self.scene.setBackgroundBrush(QBrush(QImage('IMGS/grass.jpg')))
        self.setScene(self.scene)
        self.setFixedSize(MapWindow.WIDTH, MapWindow.HEIGHT)
        self.player = None
        self.player_subjects = []
        self.player_nexus = None
        self.player_inhibitor = None
        self.player_turret = None
        self.store = None
        self.store_widget = Store(game)
        self.enemy = None
        self.enemy_subjects = []
        self.enemy_nexus = None
        self.enemy_inhibitor = None
        self.enemy_turret = None
        self.setMouseTracking(True)

    def init_map(self):
        self.player = None
        self.player_subjects = []
        self.player_nexus = None
        self.player_inhibitor = None
        self.player_turret = None
        self.store = None
        self.enemy = None
        self.enemy_subjects = []
        self.enemy_nexus = None
        self.enemy_inhibitor = None
        self.enemy_turret = None

    def keyPressEvent(self, event):
        if self.game.player_controller is not None:
            self.game.player_controller.stop_attack()
            self.player.change_direction(self.player.ref_x, self.player.ref_y)

            if not self.player.entity.moving:
                if event.key() == Qt.Key_W:
                    current_key = 'W'
                elif event.key() == Qt.Key_A:
                    current_key = 'A'
                elif event.key() == Qt.Key_S:
                    current_key = 'S'
                elif event.key() == Qt.Key_D:
                    current_key = 'D'

                if event.key() in [Qt.Key_W, Qt.Key_S, Qt.Key_A, Qt.Key_D]:
                    self.player.entity.moving = True
                    self.game.player_controller.attend_move_request(
                        current_key)

    def keyReleaseEvent(self, event):
        if self.player.entity.moving:
            self.game.player_controller.stop_movement()
            self.player.entity.moving = False

    def mouseMoveEvent(self, event):
        if not self.player.entity.moving_towards_enemy:
            QGraphicsView.mouseMoveEvent(self, event)
            x = self.mapFromGlobal(QCursor.pos()).x()
            y = self.mapFromGlobal(QCursor.pos()).y()
            self.player.change_direction(x, y)

        item = self.itemAt(self.mapFromGlobal(QCursor.pos()))
        if item is not None and hasattr(item, 'entity'):
            if item.entity in self.game.enemy_entities:
                item.setSelected(True)

    def closeEvent(self, event):
        message_box = QMessageBox()
        message_box.setWindowTitle('Exit League of Progra')
        message_box.setText('All unsaved progress will be lost. Are you sure y'
                            'ou want to quit the current game?')
        message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        value = message_box.exec_()
        if value == QMessageBox.Cancel:
            event.ignore()
        else:
            self.game.stop_game()
            self.game.cleaning_timer.stop()
            self.game_over.emit()

    def show_winner(self, winner):
        msg = QMessageBox()
        if winner == 'You':
            msg.setText('Congratulations, you won!')
        else:
            msg.setText('YOU LOSE! Good day, sir.')
        msg.exec_()
        self.game.stop_game()
        self.game.cleaning_timer.stop()
        self.hide()
        self.game_over.emit()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.itemAt(self.mapFromGlobal(QCursor.pos()))
            if item is self.store:
                self.store_widget.show()
            elif item is not None and hasattr(item, 'entity'):
                if item.entity in self.game.enemy_entities:
                    if not self.player.entity.moving_towards_enemy:
                        self.player.entity.target = item.entity
                        self.player.entity.moving_towards_enemy = True
                        self.game.player_controller.attend_attack_request(
                            item.entity
                        )

    def mouseDoubleClickEvent(self, event):
        pass

    def set_player(self, player):
        self.player = {
            'Clau': ClauItem(player),
            'Hernan': HernanItem(player)
        }[player.name]
        player.item = self.player
        x, y = self.get_location(player,
                                 int(self.WIDTH * 0.1),
                                 int(self.WIDTH * 0.15),
                                 int(self.HEIGHT * 0.3),
                                 int(self.HEIGHT * 0.4))

        """
        self.player.initialize_position(int(self.WIDTH * 0.2),
                                        int(self.HEIGHT * 0.2))
        """
        self.player.initialize_position(x, y)
        player.position = (self.player.pos().x(), self.player.pos().y())
        self.scene.addItem(self.player)
        # player.item = self.player
        self.store = StoreItem()
        self.store.setPos(int(self.WIDTH * 0.9), int(self.HEIGHT * 0.6))
        self.scene.addItem(self.store)

    def set_enemy(self, enemy):
        if enemy.name == 'Clau':
            self.enemy = ClauItem(enemy)
        else:
            self.enemy = HernanItem(enemy)
        enemy.item = self.enemy
        x, y = self.get_location(enemy,
                                 int(self.WIDTH * 0.6),
                                 int(self.WIDTH * 0.8),
                                 int(self.HEIGHT * 0.4),
                                 int(self.HEIGHT * 0.6))

        self.enemy.initialize_position(x, y)
        enemy.position = (self.enemy.pos().x(), self.enemy.pos().y())
        self.scene.addItem(self.enemy)

    def add_player_subject(self, subject):
        item = PlayerSubjectItem(subject)
        subject.item = item
        self.player_subjects.append(item)
        self.scene.addItem(item)
        self.locate_subject(subject, 0, int(self.WIDTH * 0.3), 0,
                            int(self.HEIGHT * 0.3))

    def add_player_turret(self, turret):
        item = TurretItem(turret)
        turret.item = item
        self.player_turret = item
        self.scene.addItem(item)
        self.player_turret.set_pos(int(self.WIDTH * 0.2),
                                   int(self.HEIGHT * 0.25))

    def add_player_inhibitor(self, inhibitor):
        item = InhibitorItem(inhibitor)
        inhibitor.item = item
        self.player_inhibitor = item
        self.scene.addItem(item)
        self.player_inhibitor.set_pos(int(self.WIDTH * 0.1),
                                      int(self.HEIGHT * 0.15))

    def add_player_nexus(self, nexus):
        item = NexusItem(nexus)
        nexus.item = item
        self.player_nexus = item
        self.scene.addItem(item)
        self.player_nexus.set_pos(int(self.WIDTH * 0.01),
                                  int(self.HEIGHT * 0.02))

    def add_enemy_subject(self, subject):
        item = EnemySubjectItem(subject)
        subject.item = item
        self.enemy_subjects.append(item)
        self.scene.addItem(item)
        self.locate_subject(subject, int(self.WIDTH * 0.5),
                            int(self.WIDTH * 0.9),
                            int(self.HEIGHT * 0.5), int(self.HEIGHT * 0.9))

    def add_enemy_turret(self, turret):
        item = TurretItem(turret)
        turret.item = item
        self.enemy_turret = item
        self.scene.addItem(item)
        self.enemy_turret.set_pos(int(self.WIDTH * 0.65),
                                  int(self.HEIGHT * 0.65))

    def add_enemy_inhibitor(self, inhibitor):
        item = InhibitorItem(inhibitor)
        inhibitor.item = item
        self.enemy_inhibitor = item
        self.scene.addItem(item)
        self.enemy_inhibitor.set_pos(int(self.WIDTH * 0.8),
                                     int(self.HEIGHT * 0.8))

    def add_enemy_nexus(self, nexus):
        item = NexusItem(nexus)
        nexus.item = item
        self.enemy_nexus = item
        self.scene.addItem(item)
        self.enemy_nexus.set_pos(int(self.WIDTH * 0.92),
                                 int(self.HEIGHT * 0.85))

    @staticmethod
    def locate_subject(subject, min_x, max_x, min_y, max_y):
        x, y = random.randint(min_x, max_x), random.randint(min_y, max_y)
        subject.item.set_pos(x, y)
        while subject.item.collidingItems():
            x, y = random.randint(min_x, max_x), random.randint(min_y, max_y)
            subject.item.set_pos(x, y)

    @staticmethod
    def get_location(entity, min_x, max_x, min_y, max_y):
        x, y = random.randint(min_x, max_x), random.randint(min_y, max_y)
        entity.item.set_pos(x, y)
        while entity.item.collidingItems():
            x, y = random.randint(min_x, max_x), random.randint(min_y, max_y)
            entity.item.set_pos(x, y)
        return x, y


class UnitItem(QGraphicsPixmapItem):
    BAR_WIDTH = 30

    def __init__(self, entity, path):
        super(UnitItem, self).__init__()
        self.entity = entity
        self.pix_map = QPixmap(path)
        self.width = self.pix_map.size().width()
        self.height = self.pix_map.size().height()
        self.coordinates = {
            0: (0, 0, self.width / 3, self.height),
            1: (self.width / 3, 0, self.width / 3, self.height),
            2: (2 * self.width / 3, 0, self.width / 3, self.height)
        }
        self.setPixmap(self.pix_map.copy(*self.coordinates[0]))
        self.setTransformOriginPoint(self.boundingRect().center())
        self.set_pos(200, 200)
        self.ref_x = self.pos().x() + self.boundingRect().center().x()
        self.ref_y = self.pos().y() + self.boundingRect().center().y() - 1
        self.ref_vector = (0, -1)
        self.setFlags(QGraphicsItem.ItemIsSelectable)
        self.target = None
        self.setAcceptHoverEvents(True)
        self.health_bar = QGraphicsLineItem(
            0, self.boundingRect().bottomLeft().y() + 10, self.BAR_WIDTH,
            self.boundingRect().bottomLeft().y() + 10, self)
        self.health_bar.setPen(Qt.red)
        self.count = 0

    def update_health_bar(self):
        ratio = self.entity.health / self.entity.init_health
        self.health_bar.setLine(0, self.boundingRect().bottomLeft().y() + 10,
                                self.BAR_WIDTH * ratio,
                                self.boundingRect().bottomLeft().y() + 10)

    def move(self, direction='W'):
        k = 0.5
        old_x, old_y = self.pos().x(), self.pos().y()
        distance = numpy.linalg.norm(self.ref_vector)
        if direction == 'W':
            v = (-self.ref_vector[0], -self.ref_vector[1])
        elif direction == 'S':
            v = (self.ref_vector[0], self.ref_vector[1])
        elif direction == 'D':
            v = (-self.ref_vector[1], self.ref_vector[0])
        else:
            v = (self.ref_vector[1], -self.ref_vector[0])
        n = numpy.linalg.norm(v)
        delta_x = (v[0] / n) * self.entity.speed * k
        delta_y = (v[1] / n) * self.entity.speed * k
        x = self.pos().x() + delta_x
        y = self.pos().y() + delta_y
        if distance > self.entity.speed * k:
            if direction in ['A', 'D']:
                self.move_special(direction, k)
            else:
                self.set_pos(x, y)
                self.ref_vector = \
                    (self.pos().x() + self.boundingRect().center().x() -
                     self.ref_x,
                     self.pos().y() + self.boundingRect().center().y()
                     - self.ref_y)
        if self.collidingItems():
            self.set_pos(old_x, old_y)
        self.count += 1
        self.setPixmap(self.pix_map.copy(*self.coordinates[self.count]))
        if self.count == 2:
            self.count = 0

    def change_direction(self, ref_x, ref_y):
        origin_x = self.pos().x() + self.boundingRect().center().x()
        origin_y = self.pos().y() + self.boundingRect().center().y()
        t1 = (self.ref_y - origin_y, self.ref_x - origin_x)
        t2 = (ref_y - origin_y, ref_x - origin_x)
        angle = (math.atan2(*t2) - math.atan2(*t1)) * 360 / (2 * math.pi)
        self.setRotation(self.rotation() + angle)
        self.ref_y = ref_y
        self.ref_x = ref_x
        self.ref_vector = (origin_x - self.ref_x, origin_y - self.ref_y)

    def move_special(self, direction, k):
        x1 = self.ref_vector[0]
        y1 = self.ref_vector[1]
        r = numpy.linalg.norm(self.ref_vector)
        theta = self.entity.speed * k / r
        if direction == 'D':
            theta *= -1
        x2 = x1 * math.cos(theta) - y1 * math.sin(theta)
        y2 = x1 * math.sin(theta) + y1 * math.cos(theta)
        angle = theta * 360 / (2 * math.pi)
        x2 += self.ref_x
        y2 += self.ref_y
        self.set_pos(x2 - self.boundingRect().center().x(),
                     y2 - self.boundingRect().center().y())
        self.ref_vector = (x2 - self.ref_x, y2 - self.ref_y)
        self.setRotation(self.rotation() + angle)

    def set_pos(self, x, y):
        self.setPos(x, y)
        self.entity.position = (x, y)

    def initialize_position(self, x, y):
        self.set_pos(x, y)
        self.ref_x = self.pos().x() + self.boundingRect().center().x()
        self.ref_y = self.pos().y() + self.boundingRect().center().y() - 1

    def hoverLeaveEvent(self, event):
        self.setSelected(False)


class ClauItem(UnitItem):
    def __init__(self, champion):
        super(ClauItem, self).__init__(champion, 'IMGS/woman_clean.png')


class HernanItem(UnitItem):
    def __init__(self, champion):
        super(HernanItem, self).__init__(champion, 'IMGS/man_clean.png')


class BuildingItem(QGraphicsPixmapItem):
    BAR_WIDTH = 60

    def __init__(self, entity, path):
        super(BuildingItem, self).__init__()
        self.entity = entity
        self.pix_map = QPixmap(path)
        self.width = self.pix_map.size().width()
        self.height = self.pix_map.size().height()
        self.setPixmap(self.pix_map)
        self.health_bar = QGraphicsLineItem(
            0, self.boundingRect().bottomLeft().y() + 10, self.BAR_WIDTH,
            self.boundingRect().bottomLeft().y() + 10, self)
        self.health_bar.setPen(Qt.red)

    def update_health_bar(self):
        ratio = self.entity.health / self.entity.init_health
        self.health_bar.setLine(0, self.boundingRect().bottomLeft().y() + 10,
                                self.BAR_WIDTH * ratio,
                                self.boundingRect().bottomLeft().y() + 10)

    def set_pos(self, x, y):
        self.setPos(x, y)
        self.entity.position = (x, y)


class TurretItem(BuildingItem):
    def __init__(self, entity):
        super(TurretItem, self).__init__(entity, 'IMGS/turret.png')


class NexusItem(BuildingItem):
    def __init__(self, entity):
        super(NexusItem, self).__init__(entity, 'IMGS/nexus2.png')


class InhibitorItem(BuildingItem):
    def __init__(self, entity):
        super(InhibitorItem, self).__init__(entity, 'IMGS/inhibitor.png')


class StoreItem(BuildingItem):
    def __init__(self, entity=None):
        super(StoreItem, self).__init__(entity, 'IMGS/store.png')


class PlayerSubjectItem(UnitItem):
    def __init__(self, entity):
        super(PlayerSubjectItem, self).__init__(entity,
                                                'IMGS/player_subject.png')


class EnemySubjectItem(UnitItem):
    def __init__(self, entity):
        super(EnemySubjectItem, self).__init__(entity,
                                               'IMGS/enemy_subject.png')