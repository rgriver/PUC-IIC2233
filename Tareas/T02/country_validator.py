from linked_list import *


class CountryValidator:
    def __init__(self, population):
        self.population = population
        self.open_borders = None
        self.closed_borders = None

    def validate_country(self, country):
        data = self.population.get_data()
        next(data)
        while True:
            line = next(data, None)
            if line is None:
                break
            line = LinkedList(*line)
            if country in line:
                return True
        return False


