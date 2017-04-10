class GameWriter:
    def __init__(self, world):
        self.world = world

    def save_game(self):
        with open('game_data.txt', 'w+') as file:
            self.write_world(file)
            self.write_countries(file)

    def write_countries(self, file):
        for country in self.world.countries:
            line = ''
            line += country.name + ','
            line += country.state + ','
            line += str(country.population) + ','
            line += str(country.num_dead) + ','
            line += str(country.num_infected) + ','
            line += str(country.cure_found) + ','
            line += str(country.got_cure) + ','
            line += str(country.airport_closed) + ','
            line += str(country.borders_closed) + ','
            line += country.label + ','
            line += str(country.masks_provided) + '\n'
            file.write(line)

    def write_world(self, file):
        line = ''#'Population History'
        for population in self.world.population_history:

            line += ',' + str(population)
        line = line[1:]
        file.write(line)

        line = ''#'Clean History'
        for clean in self.world.clean_history:
            line += ',' + str(clean)
        line = line[1:]
        file.write(line + '\n')

        line = ''#'Infections History'
        for infections in self.world.infections_history:
            line += ',' + str(infections)
        line = line[1:]
        file.write(line + '\n')

        line = ''#'Deaths History'
        for deaths in self.world.deaths_history:
            line += ',' + str(deaths)
        line = line[1:]
        file.write(line + '\n')

        data = ''
        data += str(self.world.time) + ','
        data += str(self.world.got_cure) + ','
        data += str(self.world.infection.infection) + ','

        data += str(self.world.research_lab.discovered) + ','
        data += str(self.world.research_lab.progress) + ','
        data += str(self.world.research_lab.cure_found) + ','
        data += str(self.world.research_lab.discovery_day) + ','
        file.write(data + '\n')