import random
from building import Nexus
from unit import ClauTheSorceress, HernanTheDestructor
import numpy
import math
from PyQt5.QtCore import QTimer
from controller import PlayerController, EnemyController, SubjectsController, \
    TurretsController, InhibitorsController


class Game:
    def __init__(self):
        self.map_window = None
        self.player = None
        self.player_subjects = []
        self.player_nexus = None
        self.player_turret = None
        self.player_inhibitor = None
        self.enemy = None
        self.enemy_subjects = []
        self.enemy_nexus = None
        self.enemy_turret = None
        self.enemy_inhibitor = None
        self.store = None
        self.player_controller = None
        self.enemy_controller = None
        self.subjects_controller = None
        self.turrets_controller = None
        self.inhibitors_controller = None
        self.nexus_controller = None
        self.enemy_entities = []
        self.player_entities = []
        self.entities = []
        self.cleaning_timer = QTimer()
        self.cleaning_timer.timeout.connect(self.remove_entities)
        self.points = 0

    def set_map_window(self, map_window):
        self.map_window = map_window

    def initialize_game(self, champion_name):
        self.points = 0
        self.map_window.scene.clear()
        self.turrets_controller = TurretsController(self)
        self.inhibitors_controller = InhibitorsController(self)
        self.create_nexus()
        self.player = {
            'Clau': ClauTheSorceress(),
            'Hernan': HernanTheDestructor()
        }[champion_name]
        self.entities.append(self.player)
        self.player_entities.append(self.player)
        self.map_window.set_player(self.player)
        self.enemy = random.choice([ClauTheSorceress(), HernanTheDestructor()])
        self.enemy_entities.append(self.enemy)
        self.map_window.set_enemy(self.enemy)
        # self.turrets_controller = TurretsController(self)
        # self.inhibitors_controller = InhibitorsController(self)
        # self.create_nexus()
        self.subjects_controller = SubjectsController(self)
        self.player_controller = PlayerController(self)
        self.enemy_controller = EnemyController(self)
        self.cleaning_timer.start(100)

    def create_nexus(self):
        nexus = Nexus()
        self.player_nexus = nexus
        self.player_entities.append(nexus)
        self.map_window.add_player_nexus(nexus)
        nexus = Nexus()
        self.enemy_nexus = nexus
        self.enemy_entities.append(nexus)
        self.map_window.add_enemy_nexus(nexus)

    def remove_entities(self):
        if self.player is not None:
            if self.player.dead:
                self.player = None
                self.player_controller.player_timer.start(10000)

        if self.player_turret is not None:
            if self.player_turret.dead:
                self.player_turret = None

        if self.player_inhibitor is not None:
            if self.player_inhibitor.dead:
                self.player_inhibitor = None
                self.inhibitors_controller.player_inhibitor_timer.start(30000)

        if self.player_nexus is not None:
            if self.player_nexus.dead:
                self.map_window.show_winner('Computer')

        if self.enemy is not None:
            if self.enemy.dead:
                self.enemy_controller.behavior.timer.stop()
                self.enemy = None
                self.enemy_controller.enemy_timer.start(10000)

        if self.enemy_turret is not None:
            if self.enemy_turret.dead:
                self.enemy_turret = None

        if self.enemy_inhibitor is not None:
            if self.enemy_inhibitor.dead:
                self.enemy_inhibitor = None
                self.inhibitors_controller.enemy_inhibitor_timer.start(30000)

        if self.enemy_nexus is not None:
            if self.enemy_nexus.dead:
                self.map_window.show_winner('You')

        for e in self.player_entities:
            if e.dead:
                scene = e.item.scene()
                scene.removeItem(e.item)
                # self.map_window.scene.removeItem(e.item)
                self.player_entities.remove(e)

        for e in self.enemy_entities:
            if e.dead:
                scene = e.item.scene()
                scene.removeItem(e.item)
                # self.map_window.scene.removeItem(e.item)
                self.enemy_entities.remove(e)

    def stop_game(self):
        for s in self.player_subjects:
            s.movement_controller = None
        for s in self.enemy_subjects:
            s.movement_controller = None
        self.player = None
        self.player_subjects = []
        self.player_entities = []
        self.enemy = None
        self.enemy_subjects = []
        self.enemy_entities = []
        self.subjects_controller = None
        self.player_controller = None
        self.enemy_controller = None
        self.turrets_controller = None
        self.inhibitors_controller = None
        self.cleaning_timer.stop()
