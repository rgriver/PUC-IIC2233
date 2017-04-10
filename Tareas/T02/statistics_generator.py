class StatisticsGenerator:
    def __init__(self, world):
        self.world = world

    def generate_summary(self):
        summary = '******* Day ' + str(self.world.time) + ' *******\n'
        summary += 'Infections: ' + str(self.world.new_infections) + '\n'
        summary += 'Deaths: ' + str(self.world.new_deaths) + '\n'
        if self.world.new_infected_countries:
            summary += 'Infected countries:\n'
            for country in self.world.new_infected_countries:
                summary += '    ' + country.name + '\n'
        if self.world.new_closed_airports:
            summary += 'Closed airports:\n'
            for country in self.world.new_closed_airports:
                summary += '    ' + country.name + '\n'
        if self.world.new_closed_borders:
            summary += 'Closed borders:\n'
            for country in self.world.new_closed_borders:
                summary += '    ' + country.name + '\n'
        if self.world.new_masks:
            summary += 'Countries with masks:\n'
            for country in self.world.new_masks:
                summary += '    ' + country.name + '\n'
        print(summary)
        print('----------------------------------------\n')

    def print_world_population_state(self):
        info = 'Clean people: ' + \
               str(self.world.population - self.world.num_infected) + '\n'
        info += 'Infected people: ' + str(self.world.num_infected) + '\n'
        info += 'Dead people: ' + str(self.world.num_dead) + '\n'
        print(info)
        print('----------------------------------------\n')

    def print_country_state(self, country_name):
        for country in self.world.countries:
            if country.name == country_name:
                info = 'Population: ' + str(country.population) + '\n'
                info += 'Infected: ' + str(country.num_infected) + '\n'
                info += 'Dead: ' + str(country.num_dead) + '\n'
                print(info)
                print('----------------------------------------\n')

    def print_clean_countries(self):
        info = 'Clean Countries:\n'
        for country in self.world.countries:
            if country.state == 'Clean':
                info += '    ' + country.name + '\n'
        if info == 'Clean Countries:\n':
            info = 'No clean countries\n'
        print(info)
        print('----------------------------------------\n')

    def print_infected_countries(self):
        info = 'Infected Countries:\n'
        for country in self.world.countries:
            if country.state == 'Infected':
                info += '    ' + country.name + ' ' + \
                        str(country.get_infection_ratio() * 100) + '% ' + \
                        'affected' + '\n'
        if info == 'Infected Countries:\n':
            info = 'No infected countries\n'
        print(info)
        print('----------------------------------------\n')

    def print_dead_countries(self):
        info = 'Dead Countries:\n'
        for country in self.world.countries:
            if country.state == 'Dead':
                info += '    ' + country.name + '\n'
        if info == 'Dead Countries:\n':
            info = 'No dead countries\n'
        print(info)
        print('----------------------------------------\n')

    def print_population_info(self):
        info = 'World population: ' + str(self.world.population) + '\n'
        info += 'Clean: ' + \
                str(self.world.population - self.world.num_infected) + '\n'
        info += 'Infected: ' + str(self.world.num_infected) + '\n'
        info += 'Dead: ' + str(self.world.num_dead) + '\n'
        print(info)
        print('----------------------------------------\n')

    def print_deaths_and_infections(self):
        info = ''
        for day in range(len(self.world.infections_history)):
            info += '******* Day ' + str(day) + ' *******\n'
            info += 'Infections: ' + str(self.world.infections_history[day]) \
                    + '\n'
            info += 'Deaths: ' + str(self.world.deaths_history[day]) + '\n\n'
        print(info)
        print('----------------------------------------\n')

    def print_measures(self, name):
        info = 'Rejected measures\n'
        for country in self.world.countries:
            if country.name == name:
                if country.measures_list:
                    for measure in country.measures_list:
                        if not measure.accepted:
                            info += 'Type: ' + measure.type + '\n'
                            info += 'Priority: ' + str(measure.priority) + \
                                    '\n\n'
                else:
                    info = 'No measures created' + '\n'
        if info == 'Rejected measures\n':
            info = 'No rejected measures'
        print(info)
        print('----------------------------------------\n')

    def print_di_rates(self):
        cumulative = 0
        for infections in self.world.infections_history:
            cumulative += infections
        cumulative /= (self.world.time + 1)
        info = 'Cumulative: ' + str(int(cumulative)) + ' infections per day\n'

        size = len(self.world.infections_history)
        actual = self.world.infections_history[size - 1] / \
            len(self.world.countries)
        info += 'Today: ' + str(int(actual)) + ' infections per country\n'
        print(info)
        print('----------------------------------------\n')

