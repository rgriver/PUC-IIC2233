class Infection:
    def __init__(self, infection):
        self.infection = infection
        self.contagiousness = None
        self.mortality = None
        self.resistance = None
        self.visibility = None
        self.set_infection()

    def set_infection(self):
        if self.infection == 'Virus':
            self.contagiousness = 1.5
            self.mortality = 1.2
            self.resistance = 1.5
            self.visibility = 0.5
        elif self.infection == 'Bacteria':
            self.contagiousness = 1.0
            self.mortality = 1.0
            self.resistance = 0.5
            self.visibility = 0.7
        else:
            self.contagiousness = 0.5
            self.mortality = 1.5
            self.resistance = 1.0
            self.visibility = 0.45
