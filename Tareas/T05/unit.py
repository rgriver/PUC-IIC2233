import numpy
from PyQt5.QtCore import QTimer
from damage_manager import DamageManager
import math


class Unit:
    def __init__(self, speed, damage, attack_rate, attack_distance, health,
                 position):
        self.speed = speed
        self.damage = damage
        self.attack_rate = attack_rate
        self.attack_distance = attack_distance
        self.health = health
        self.init_health = health
        self._position = None
        self.item = None
        self.moving = False
        self.moving_towards_enemy = False
        self.target = None
        self.entity_attacked = None
        self.dead = False

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def attack(self, character):
        self.entity_attacked = character
        damage_manager = DamageManager(self, character)
        damage_manager.apply_damage()


class ClauTheSorceress(Unit):
    def __init__(self):
        self.name = 'Clau'
        super(ClauTheSorceress, self).__init__(
            speed=30,
            attack_distance=40,
            attack_rate=10,
            damage=35,  # 5
            health=500,
            position=[452, 342]
        )

    def special_attack(self):
        pass


class HernanTheDestructor(Unit):
    def __init__(self):
        self.name = 'Hernan'
        super(HernanTheDestructor, self).__init__(
            speed=10,
            damage=20,
            attack_distance=35,#5
            attack_rate=10,
            health=666,
            position=[60, 62]
        )

    def special_attack(self):
        pass

    
class NormalSubject(Unit):
    def __init__(self):
        super(NormalSubject, self).__init__(
            speed=8,
            damage=2,
            attack_distance=5,  # 5
            attack_rate=1,
            health=45,
            position=(0, 0)
        )
        self.name = 'NormalSubject'
        self.item = None
        self.movement_controller = MovementController(self)


class LargeSubject(Unit):
    def __init__(self, item):
        super(LargeSubject, self).__init__(
            speed=8,
            damage=4,
            attack_distance=20,  # 5
            attack_rate=1,
            health=60,
            position=(0, 0)
        )
        self.name = 'LargeSubject'
        self.item = item

    def move(self, direction):
        self.item.change_direction(direction)
        self.item.move()


class MovementController:
    def __init__(self, entity):
        self.entity = entity
        self.timer = QTimer()
        self.timer.start(100)
        self.timer.timeout.connect(self.play)

    def play(self):
        self.entity.item.change_direction(*self.entity.target.position)
        if self.dist2(self.entity.item, self.entity.target.item) >= \
                self.entity.attack_distance:
            self.entity.entity_attacked = None
            self.entity.item.move()
        else:
            self.entity.attack(self.entity.target)

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

