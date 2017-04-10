class Measure:
    def __init__(self, country, measure_type):
        self.country = country
        self.type = measure_type
        self.accepted = False
        self.priority = self.calculate_priority()

    def accept(self):
        self.accepted = True
        if self.type == 'Close airport':
            self.country.airport_closed = True
        elif self.type == 'Open airport':
            self.country.airport_closed = False
        elif self.type == 'Close borders':
            self.country.airport_closed = True
        elif self.type == 'Open borders':
            self.country.borders_closed = False
        elif self.type == 'Provide masks':
            self.country.provide_masks()

    def calculate_priority(self):
        if self.type == 'Close airport':
            value = 0.8
        elif self.type == 'Close borders':
            value = self.calculate_average()
        elif self.type == 'Provide masks':
            value = 0.5
        else:
            if self.country.cure_found:
                value = 1
            else:
                value = 0.7
        priority = (value * self.country.num_infected) / \
            self.country.population
        return priority

    def calculate_average(self):
        value = 0
        if self.country.neighbors:
            for neighbor in self.country.neighbors:
                if not neighbor.population:
                    break
                value += neighbor.num_infected / neighbor.population
            value /= len(self.country.neighbors)
        # Not sure if map objects are allowed
        # value = sum(map(lambda x: x.num_infected / x.population,
        #                 self.country.neighbors)) / len(self.country.neighbors)
        return value





