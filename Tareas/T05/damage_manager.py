class DamageManager:
    def __init__(self, attacker, attacked):
        self.attacker = attacker
        self.attacked = attacked

    def apply_damage(self):
        damage = self.attacker.damage * 0.1
        if self.attacked.health - damage < 0:
            self.attacked.health = 0
            self.attacked.dead = True
            self.attacker.target = None
        else:
            self.attacked.health -= damage
        self.attacked.item.update_health_bar()
