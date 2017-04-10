from connections_generator import *
from country_validator import *
from borders_database import *
from linked_list import *
from connections_generator import generate_connections
from countries_creator import *
from world import *
from game_loader import *
from population_database import *
from airports_database import *
from infection import *
from statistics_generator import *
from game_writer import *

class Game:
    def __init__(self):
        self.world = None
        self.statistics_generator = None#StatisticsGenerator(self)
        self.borders = BordersDatabase()
        self.airports = AirportsDatabase('airports.csv')
        self.population = PopulationDatabase('population.csv')
        self.world = None
        self.countries = LinkedList()
        self.infection = None

    def create_new_game(self, infection, name):
        cv = CountryValidator(self.population)
        validation_state = cv.validate_country(name)
        if validation_state:  # We're good
            self.infection = Infection(infection)
            generate_connections()
            cc = CountriesCreator(self.borders, self.airports, self.population)
            self.countries = cc.create_countries()
            self.world = World(self.countries, self.infection)
            for country in self.countries:
                if country.name == name:
                    country.state = 'Infected'
                    country.infect_people(1)
                    break
            self.world.update_connections()
            self.world.update_data()
            self.world.update_history()
            return True
        return False

    def load_saved_game(self):
        gl = GameLoader()
        if gl.load_game():
            return True
        return False

    def save_game(self):
        gs = GameWriter(self.world)
        gs.save_game()

    def play(self):
        self.world.add_time()
        self.world.clean_data()
        #self.world.update_history()
        self.world.update_connections()
        self.world.propagate_infection()
        self.world.apply_damage()
        self.world.propagate_cure()
        self.world.fight_infection()
        self.world.update_data()
        self.world.update_history()
        #self.world.add_time()

    def generate_summary(self):
        stats_gen = StatisticsGenerator(self.world)
        stats_gen.generate_summary()

    def generate_country_state(self, country_name):
        stats_gen = StatisticsGenerator(self.world)
        stats_gen.print_country_state(country_name)

    def print_clean_countries(self):
        stats_gen = StatisticsGenerator(self.world)
        stats_gen.print_clean_countries()


    def print_infected_countries(self):
        stats_gen = StatisticsGenerator(self.world)
        stats_gen.print_infected_countries()


    def print_dead_countries(self):
        stats_gen = StatisticsGenerator(self.world)
        stats_gen.print_dead_countries()

    def print_population_info(self):
        stats_gen = StatisticsGenerator(self.world)
        stats_gen.print_population_info()

    def print_deaths_and_infections(self):
        stats_gen = StatisticsGenerator(self.world)
        stats_gen.print_deaths_and_infections()

    def print_measures(self, name):
        stats_gen = StatisticsGenerator(self.world)
        stats_gen.print_measures(name)

    def print_di_rates(self):
        stats_gen = StatisticsGenerator(self.world)
        stats_gen.print_di_rates()

    def won(self):
        for country in self.countries:
            if country.state != 'Dead':
                return False
        return True

    def lost(self):
        for country in self.countries:
            if country.num_infected != 0 and country.population != 0:
                return False
        return True
