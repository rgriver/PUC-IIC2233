from country import *
from linked_list import *
from government import *
from linked_list import *

class Country:
    def __init__(self, name):
        self.name = name
        self.state = 'Clean'
        self.num_dead = 0
        self.num_infected = 0
        self.neighbors = LinkedList()
        self.cure_found = False
        self.got_cure = False
        self.airport = None
        self.airport_closed = False
        self.flight_routes = LinkedList()
        self.population = 0
        self.init_population = 0
        self.borders_closed = False
        self.label = 'Unvisited'
        self.connections = LinkedList()
        self.government = Government(self)
        self.masks_provided = False
        self.measures_list = LinkedList()

    def update_connections(self):
        self.connections = LinkedList()
        if not self.borders_closed:
            self.connections.add_list(self.neighbors)
        if self.airport is True:
            if not self.airport_closed:
                self.connections.add_list(self.flight_routes)

    def get_measures(self):
        self.government.generate_measures()
        return self.measures_list

    def get_neighbors(self):
        return self.neighbors

    def get_routes(self):
        return self.flight_routes

    def set_state(self, state):
        self.state = state

    def kill_people(self, num_people):
        if self.num_infected > 0:
            self.num_dead += num_people
            self.population -= num_people
            self.num_infected -= num_people
            if self.population <= 0:
                self.state = 'Dead'
            # No infected people means clean country.
            elif self.num_infected <= 0:
                self.state = 'Clean'
                self.num_infected = 0

    def get_infection_ratio(self):
        ratio = (self.num_infected + self.num_dead) / self.init_population
        return ratio

    def infect_people(self, num_people):
        if self.num_infected + num_people < self.population:
            self.num_infected += num_people
        else:
            self.num_infected = self.population

    def cure_people(self, num_people):
        if self.num_infected - num_people < 0:
            self.num_infected = 0
        else:
            self.num_infected -= num_people

    def provide_masks(self):
        self.masks_provided = True

