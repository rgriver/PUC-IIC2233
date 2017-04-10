from measure import *
from linked_list import *

class Government:
    def __init__(self, country):
        self.country = country

    def generate_measures(self):
        self.country.measures_list = LinkedList()
        infected = self.country.num_infected / self.country.init_population
        dead = self.country.num_dead / self.country.init_population
        if infected > 0.5 or dead > 0.25:
            measure = Measure(self.country, 'Close borders')
            self.country.measures_list.add_tail(measure)
        else:
            measure = Measure(self.country, 'Open borders')
            self.country.measures_list.add_tail(measure)
        if self.country.airport is True:
            if infected > 0.8 or dead > 0.2:
                measure = Measure(self.country, 'Close airport')
                self.country.measures_list.add_tail(measure)
            else:
                measure = Measure(self.country, 'Open airport')
                self.country.measures_list.add_tail(measure)
        if infected > 1/3:
            measure = Measure(self.country, 'Provide masks')
            self.country.measures_list.add_tail(measure)

