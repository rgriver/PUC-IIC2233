from PyQt5.QtCore import QTimer
from unit import NormalSubject, ClauTheSorceress, HernanTheDestructor
from building import Inhibitor, Turret
import numpy
import math
import random


class Controller:
    @staticmethod
    def dist(a, b):
        d = numpy.subtract(a, b)
        d = numpy.linalg.norm(d)
        return d

    def dist2(self, item1, item2):
        p1 = item1.pos() + item1.boundingRect().center()
        p2 = item2.pos() + item2.boundingRect().center()
        dx1, dy1 = self.helper(item1)
        dx2, dy2 = self.helper(item2)
        x = max(abs(p1.x() - p2.x()) - (dx1 + dx2), 0)
        y = max(abs(p1.y() - p2.y()) - (dy1 + dy2), 0)
        d = numpy.linalg.norm((x, y))
        # print(d)
        return d

    @staticmethod
    def helper(item):
        dy = max(abs(0.5 * item.boundingRect().height() * math.cos(
            item.rotation() * 2 * math.pi / 360)),
                 abs(0.5 * item.boundingRect().width() * math.cos(
                     item.rotation() * 2 * math.pi / 360 - 0.5 * math.pi)))
        dx = max(abs(0.5 * item.boundingRect().height() * math.sin(
            item.rotation() * 2 * math.pi / 360)),
                 abs(0.5 * item.boundingRect().width() * math.sin(
                     item.rotation() * 2 * math.pi / 360 - 0.5 * math.pi)))

        return dx, dy


class EnemyController(Controller):
    def __init__(self, game):
        self.game = game
        self.enemy = game.enemy
        self.name = self.enemy.name
        self.behavior = random.choice([ProBehavior(game), NoobBehavior(game)])
        self.enemy_timer = QTimer()
        self.enemy_timer.setSingleShot(True)
        self.enemy_timer.timeout.connect(self.create_enemy)

    def set_position(self, value):
        self.enemy.position = value

    def create_enemy(self):
        if self.name == 'Clau':
            self.game.enemy = ClauTheSorceress()
        else:
            self.game.enemy = HernanTheDestructor()
        self.game.enemy_entities.append(self.game.enemy)
        self.game.map_window.set_enemy(self.game.enemy)
        self.behavior.timer.start(100)


class NoobBehavior:
    def __init__(self, game):
        self.enemy = game.enemy
        self.player_entities = game.player_entities
        self.map_window = game.map_window
        self.timer = QTimer()
        self.timer.start(100)
        self.timer.timeout.connect(self.play)

    def play(self):
        entity = self.choose_entity()
        self.map_window.enemy.change_direction(*entity.position)
        if self.dist(self.enemy.position, entity.position) >= \
                self.enemy.attack_distance:
            self.enemy.entity_attacked = None
            self.map_window.enemy.move()
        else:
            self.enemy.attack(entity)

    def choose_entity(self):
        l = [(e, numpy.linalg.norm(numpy.subtract(self.enemy.position,
              e.position))) for e in self.player_entities]
        entity = min(l, key=lambda x: x[1])[0]
        return entity

    @staticmethod
    def dist(a, b):
        d = numpy.subtract(a, b)
        d = numpy.linalg.norm(d)
        return d


class ProBehavior:
    def __init__(self, game):
        self.game = game
        self.timer = QTimer()
        self.timer.start(100)
        self.timer.timeout.connect(self.play)

    def play(self):
        if [e for e in self.game.enemy_subjects if e.target is
                self.game.player_turret]:
            self.game.enemy.target = self.game.player_turret
        elif not [e for e in self.game.enemy_subjects if
                  self.dist2(self.game.enemy.item,
                             e.item) <= self.game.enemy.attack_distance]:
            targets = [e for e in self.game.player_entities if
                       e.health / e.health >= 0.2 * e.init_health or (
                           self.game.enemy.health > e.health)]
            l = [(e, self.dist2(self.game.enemy.item, e.item)) for e in
                 targets]
            if l:
                self.game.enemy.target = min(l, key=lambda x: x[1])[0]
        if self.game.enemy.target is not None:
            self.game.map_window.enemy.change_direction(
                *self.game.enemy.target.position)
            if self.dist2(self.game.enemy.item, self.game.enemy.target.item) \
                    >= self.game.enemy.attack_distance:
                self.game.enemy.entity_attacked = None
                self.game.map_window.enemy.move()
            else:
                self.game.enemy.attack(self.game.enemy.target)

    def dist2(self, item1, item2):
        p1 = item1.pos() + item1.boundingRect().center()
        p2 = item2.pos() + item2.boundingRect().center()
        dx1, dy1 = self.helper(item1)
        dx2, dy2 = self.helper(item2)
        x = max(abs(p1.x() - p2.x()) - (dx1 + dx2), 0)
        y = max(abs(p1.y() - p2.y()) - (dy1 + dy2), 0)
        d = numpy.linalg.norm((x, y))
        # print(d)
        return d

    @staticmethod
    def helper(item):
        dy = max(abs(0.5 * item.boundingRect().height() * math.cos(
            item.rotation() * 2 * math.pi / 360)),
                 abs(0.5 * item.boundingRect().width() * math.cos(
                     item.rotation() * 2 * math.pi / 360 - 0.5 * math.pi)))
        dx = max(abs(0.5 * item.boundingRect().height() * math.sin(
            item.rotation() * 2 * math.pi / 360)),
                 abs(0.5 * item.boundingRect().width() * math.sin(
                     item.rotation() * 2 * math.pi / 360 - 0.5 * math.pi)))

        return dx, dy


class PlayerController(Controller):
    def __init__(self, game):
        self.game = game
        self.name = game.player.name
        self.map_window = game.map_window
        self.attack_timer = QTimer()
        self.simple_move_timer = QTimer()
        self.attack_timer.timeout.connect(self.move_towards)
        self.simple_move_timer.timeout.connect(self.simple_move)
        self.target = None
        self.current_key = None
        self.player_timer = QTimer()
        self.player_timer.setSingleShot(True)
        self.player_timer.timeout.connect(self.create_player)

    def attend_attack_request(self, entity):
        self.target = entity
        self.attack_timer.start(100)

    def attend_move_request(self, current_key):
        self.simple_move_timer.start(100)
        self.current_key = current_key

    # CHANGED!!!!!
    def move_towards(self):
        if self.game.player is None:
            return 0
        if self.game.player.target is None:
            return 0
        if self.dist2(self.game.player.item,
           self.game.player.target.item) >= \
           self.game.player.attack_distance:
            self.game.player.item.change_direction(self.target.item.pos().x(),
                                                   self.target.item.pos().y())
            self.game.player.item.move()
        else:
            if self.game.player.target is None:
                self.attack_timer.stop()
            else:
                if self.target.name != 'Nexus' or self.game.enemy_inhibitor\
                        is None:
                    name = self.game.player.target.name
                    self.game.player.attack(self.game.player.target)
                    if self.game.player.target is None:
                        points = 0
                        if name in ['ClauTheSorceress', 'HernanTheDestructor']:
                            points = 5
                        elif name in ['NormalSubject', 'LargeSubject']:
                            points = 1
                        self.game.points += points

    def simple_move(self):
        self.map_window.player.move(self.current_key)

    def stop_movement(self):
        self.attack_timer.stop()
        self.simple_move_timer.stop()

    def stop_attack(self):
        self.attack_timer.stop()
        if self.game.player is not None:
            self.game.player.moving_towards_enemy = False

    def create_player(self):
        print('new player')
        if self.name == 'Clau':
            self.game.player = ClauTheSorceress()
        else:
            self.game.player = HernanTheDestructor()
        self.game.player_entities.append(self.game.enemy)
        self.game.map_window.set_player(self.game.enemy)


class SubjectsController(Controller):
    def __init__(self, game):
        self.game = game
        self.map_window = game.map_window
        self.creation_timer = QTimer()
        self.creation_timer.timeout.connect(self.create_subjects)
        self.creation_timer.start(20000)
        self.control_timer = QTimer()
        self.control_timer.timeout.connect(self.control_subjects)
        self.control_timer.start(100)  # 100 ms update
        self.create_subjects()

    def create_subjects(self):
        for i in range(4):
            subject = NormalSubject()
            self.game.player_subjects.append(subject)
            self.game.player_entities.append(subject)
            self.map_window.add_player_subject(subject)

        for i in range(4):
            subject = NormalSubject()
            self.game.enemy_subjects.append(subject)
            self.game.enemy_entities.append(subject)
            self.map_window.add_enemy_subject(subject)

    def control_subjects(self):
        for subject in self.game.player_subjects:
            l = [e for e in self.game.enemy_entities if e.entity_attacked is
                 self.game.player]
            if l and self.game.player is not None:
                entity = self.choose_nearest_entity(subject, l)
                subject.target = entity
            else:
                entity = self.choose_nearest_entity(subject,
                                                    self.game.enemy_entities)
                subject.target = entity

        for subject in self.game.enemy_subjects:
            l = [e for e in self.game.player_entities if e.entity_attacked is
                 self.game.enemy]
            if l and self.game.enemy is not None:
                entity = self.choose_nearest_entity(subject, l)
                subject.target = entity
            else:
                entity = self.choose_nearest_entity(subject,
                                                    self.game.player_entities)
                subject.target = entity

    def choose_nearest_entity(self, subject, l):
        # l2 = [(e, numpy.linalg.norm(numpy.subtract(subject.position,
        #                            e.position))) for e in l]
        l2 = [(e, self.dist2(subject.item, e.item)) for e in l]
        entity = None
        if l2:
            entity = min(l2, key=lambda x: x[1])[0]
        return entity


class TurretsController(Controller):
    def __init__(self, game):
        self.game = game
        self.create_turrets()
        self.timer = QTimer()
        self.timer.timeout.connect(self.play)
        self.timer.start(1000)

    def create_turrets(self):
        turret = Turret()
        self.game.player_turret = turret
        self.game.player_entities.append(turret)
        self.game.map_window.add_player_turret(turret)
        turret = Turret()
        self.game.enemy_turret = turret
        self.game.enemy_entities.append(turret)
        self.game.map_window.add_enemy_turret(turret)

    def control_turret(self, turret, champion, entities):
        l = [e for e in entities if e.entity_attacked is champion]
        if l:
            l2 = [(e, self.dist2(turret.item, e.item)) for e in l]
            l2 = [t for t in l2 if t[1] <= turret.attack_distance]
            if l2:
                entity = min(l2, key=lambda x: x[1])[0]
                turret.target = entity
                turret.attack()
        else:
            l2 = [(e, self.dist2(turret.item, e.item)) for e
                  in entities]
            l2 = [t for t in l2 if t[1] <= turret.attack_distance]
            if l2:
                entity = min(l2, key=lambda x: x[1])[0]
                turret.target = entity
                turret.attack()

    def play(self):
        if self.game.player_turret is not None:
            self.control_turret(self.game.player_turret, self.game.player,
                                self.game.enemy_entities)

        if self.game.enemy_turret is not None:
            self.control_turret(self.game.enemy_turret, self.game.enemy,
                                self.game.player_entities)

        if self.game.player_turret is None and self.game.enemy_turret is None:
            self.timer.stop()


class InhibitorsController:
    def __init__(self, game):
        self.game = game
        self.player_inhibitor_timer = QTimer()
        self.player_inhibitor_timer.setSingleShot(True)
        self.player_inhibitor_timer.timeout.connect(
            self.create_player_inhibitor)
        self.enemy_inhibitor_timer = QTimer()
        self.enemy_inhibitor_timer.setSingleShot(True)
        self.enemy_inhibitor_timer.timeout.connect(
            self.create_enemy_inhibitor)
        self.create_player_inhibitor()
        self.create_enemy_inhibitor()

    def create_player_inhibitor(self):
        inhibitor = Inhibitor()
        self.game.player_inhibitor = inhibitor
        self.game.player_entities.append(inhibitor)
        self.game.map_window.add_player_inhibitor(inhibitor)

    def create_enemy_inhibitor(self):
        inhibitor = Inhibitor()
        self.game.enemy_inhibitor = inhibitor
        self.game.enemy_entities.append(inhibitor)
        self.game.map_window.add_enemy_inhibitor(inhibitor)

