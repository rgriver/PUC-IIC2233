from random import random


class HealingCalculator:
    def __init__(self, countries, infection):
        self.countries = countries
        self.infection = infection

    def apply_cure(self):
        for country in self.countries:
            if country.got_cure and country.num_infected and country.population:
                # Slow method
                # for person in range(country.num_infected):
                #     if random() <= 0.25 * self.infection.resistance:
                #         country.cure_people(1)
                mean = 0
                if country.num_infected < 10:
                    num_people = int(country.num_infected)
                else:
                    num_people = int(max(0.000001 * country.num_infected, 10))
                for person in range(num_people):
                    mean += int(random() < 0.25 * self.infection.resistance)
                mean /= num_people
                num_people_to_cure = mean * country.num_infected
                country.cure_people(int(num_people_to_cure))
            else:
                continue


'''
En este caso sucede lo mismo. La cantidad de personas infectadas provoca que
el tiempo de ejecución del loop sea muy largo. Como en los otros casos, una
opción es tomar un promedio de un conjunto reducido.
'''
