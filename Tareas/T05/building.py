from damage_manager import DamageManager


class Inhibitor:
    def __init__(self):
        self.name = 'Inhibitor'
        self.dead = False
        self.health = 600
        self.init_health = 600
        self.item = None
        self.position = (0, 0)
        self.entity_attacked = None


class Turret:
    def __init__(self):
        self.name = 'Turret'
        self.damage = 30
        self.health = 250
        self.init_health = 250
        self.attack_distance = 40
        self.target = None
        self.item = None
        self.dead = False
        self.position = (0, 0)
        self.entity_attacked = None

    def attack(self):
        damage_manager = DamageManager(self, self.target)
        damage_manager.apply_damage()


class Nexus:
    def __init__(self):
        self.name = 'Nexus'
        self.health = 1200
        self.init_health = 1200
        self.dead = False
        self.position = (0, 0)
        self.entity_attacked = None
