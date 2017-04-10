from linked_list import *
from country import *
from air_connections_database import *


class CountriesCreator:
    def __init__(self, borders, airports, population):
        self.borders = borders
        self.airports = airports
        self.population = population
        self.countries = LinkedList()
        self.air_connections = AirConnectionsDatabase('random_airports.csv')

    def create_countries(self):

        data = self.population.get_data()
        next(data)
        while True:
            info = next(data, None)
            if info is None:
                break
            info = LinkedList(*info)
            country = self.add_country(info[0])
            country.population = int(info[1])
            country.init_population = int(info[1])

        '''
        data = self.population.get_data()
        next(data)
        while True:
            info = next(data, None)
            if info is None:
                break
            info = LinkedList(*info)
            for country in self.countries:
                if country.name == info[0]:
                    country.population = int(info[1])
                    break
        '''

        data = self.borders.get_data()
        next(data)
        while True:
            info = next(data, None)
            if info is None:
                break
            info = LinkedList(*info)
            country_a = self.get_country(info[0])
            country_b = self.get_country(info[1])
            self.add_neighbor(country_a, country_b)
            self.add_neighbor(country_b, country_a)

        data = self.airports.get_data()
        next(data)
        while True:
            info = next(data, None)
            if info is None:
                break
            info = LinkedList(*info)
            for country in self.countries:
                if country.name.lower() == info[0].lower():
                    country.airport = True
                    break

        data = self.air_connections.get_data()
        next(data)
        while True:
            info = next(data, None)
            if info is None:
                break
            info = LinkedList(*info)
            self.add_air_connections(info[0], info[1])

        return self.countries

    def add_country(self, country_name):
        for country in self.countries:
            if country.name == country_name:
                return country
        country = Country(country_name)
        self.countries.add_tail(country)
        return country

    @staticmethod
    def add_neighbor(country, new_neighbor):
        for neighbor in country.neighbors:
            if neighbor == new_neighbor:
                return False
        country.neighbors.add_tail(new_neighbor)
        return True

    def add_air_connections(self, name_a, name_b):
        for c in self.countries:
            if c.name == name_a:
                country_a = c
            if c.name == name_b:
                country_b = c
        country_a.flight_routes.add_tail(country_b)
        country_b.flight_routes.add_tail(country_a)

    def get_country(self, name):
        for country in self.countries:
            if country.name == name:
                return country
        return None



