from random import randint, random


class ResearchLab:
    def __init__(self, world):
        self.world = world
        self.infection = world.infection
        self.discovered = False
        self.progress = 0
        self.cure_found = False
        self.discovery_day = 0

    def work(self):
        if not self.discovered:
            probability = self.calculate_discovery_probability()
            if random() < probability:
                self.discovered = True
                self.discovery_day = self.world.time
        else:
            if not self.cure_found:
                self.work_on_a_cure()
                if self.progress >= 100:
                    self.cure_found = True
                    self.world.got_cure = True
                    for country in self.world.countries:
                        country.cure_found = True
                    size = len(self.world.countries)
                    index = randint(0, size - 1)
                    chosen_country = self.world.countries[index]
                    chosen_country.got_cure = True

    def calculate_discovery_probability(self):
        probability = (self.infection.visibility * self.world.num_infected *
                       self.world.num_dead ** 2) / self.world.init_population
        return probability

    def work_on_a_cure(self):
        progress = 0
        for t in range(self.discovery_day, self.world.time):
            progress += (100 * self.world.clean_history[t]) / \
                     (2 * self.world.init_population)
        self.progress = progress

    def set_progress(self, progress):
        self.progress = progress


