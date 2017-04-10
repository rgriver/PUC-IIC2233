from country_list import *
from infection_calculator import *
from research_lab import *
from measures_list import *
from healing_calculator import *


class World:
    def __init__(self, countries, infection):
        self.countries = countries
        self.population = 0
        self.deaths = 0
        self.discovery_level = 0
        self.infection = infection
        self.time = 0
        self.infection_calculator = InfectionCalculator(self)
        self.healing_calculator = HealingCalculator(countries, infection)
        self.research_lab = ResearchLab(self)
        self.num_infected = 0
        self.num_dead = 0
        self.population_history = LinkedList()
        self.clean_history = LinkedList()
        self.measures_list = MeasuresList()
        self.got_cure = False
        self.init_population = self.get_init_population()
        self.new_infections = 0
        self.new_deaths = 0
        self.new_infected_countries = LinkedList()
        self.new_closed_borders = LinkedList()
        self.new_closed_airports = LinkedList()
        self.new_masks = LinkedList()
        self.infections_history = LinkedList()
        self.deaths_history = LinkedList()

    def propagate_infection(self):
        for country in self.countries:
            if country.state == 'Infected':
                self.dfs(country)
            else:
                continue
        for country in self.countries:
            country.label = 'Unvisited'

    def dfs(self, country):
        country.label = 'Visited'
        for connection in country.connections:
            if connection.label == 'Unvisited':
                connection.label = 'Visited'
                if connection.state == 'Clean':
                    if not self.can_spread(country, connection):
                        continue
                    if not self.infection_calculator.infect(connection):
                        continue
                    else:
                        self.new_infected_countries.add_tail(connection)
                        self.dfs(connection)

    def update_connections(self):
        for country in self.countries:
            country.update_connections()

    def apply_damage(self):
        for country in self.countries:
            self.infection_calculator.apply_damage(country)

    def fight_infection(self):
        self.research_lab.work()
        if self.got_cure:
            self.healing_calculator.apply_cure()

        self.measures_list = MeasuresList()
        for country in self.countries:
            if country.state != 'Dead':
                measures = country.get_measures()
                if measures:
                    self.measures_list.add_list(measures)
        if self.measures_list:
            self.measures_list.sort()
            top_measures = self.measures_list.get_top()
            # print(list(map(lambda x: x.priority, top_measures)))
            for measure in top_measures:
                measure.accept()
                if measure.type == 'Close borders':
                    self.new_closed_borders.add_tail(measure.country)
                elif measure.type == 'Close airport':
                    self.new_closed_airports.add_tail(measure.country)
                elif measure.type == 'Provide masks':
                    self.new_masks.add_tail(measure.country)

    def add_time(self):
        self.time += 1

    def propagate_cure(self):
        for country in self.countries:
            if country.got_cure and not country.airport_closed:
                self.dfs_cure(country)
            else:
                continue
        for country in self.countries:
            country.label = 'Unvisited'

    def dfs_cure(self, country):
        country.label = 'Visited'
        for country in country.flight_routes:
            if country.label == 'Unvisited':
                country.label = 'Visited'
                if not country.got_cure and not country.airport_closed:
                    country.got_cure = True
                else:
                    continue

    def get_init_population(self):
        init_population = 0
        for country in self.countries:
            init_population += country.population
        return init_population

    def update_data(self):
        old_num_infected = self.num_infected
        old_num_dead = self.num_dead
        self.population = 0
        self.num_infected = 0
        self.num_dead = 0
        for country in self.countries:
            self.population += country.population
            self.num_infected += country.num_infected
            self.num_dead += country.num_dead
        if self.num_dead - old_num_dead > 0:
            self.new_deaths = self.num_dead - old_num_dead
        else:
            self.new_deaths = 0
        if self.num_infected - old_num_infected > 0:
            self.new_infections = self.num_infected - old_num_infected
        else:
            self.new_infections = 0

    def update_history(self):
        self.population_history.add_tail(self.population)
        self.clean_history.add_tail(self.population - self.num_infected)
        self.infections_history.add_tail(self.new_infections)
        self.deaths_history.add_tail(self.new_deaths)

    def clean_data(self):
        self.new_infected_countries = LinkedList()
        self.new_closed_airports = LinkedList()
        self.new_closed_borders = LinkedList()

    def get_infected_ratio(self):
        ratio = (self.num_infected + self.num_dead) / self.init_population
        return ratio

    def can_spread(self, country, connection):
        if (self.get_infected_ratio() >= 0.04) and\
                (connection in country.flight_routes):
            return True
        if (country.get_infection_ratio() > 0.2) and\
                (connection in country.neighbors):
            return True
        return False
