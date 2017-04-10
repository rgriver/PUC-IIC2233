from random import randint, random


class InfectionCalculator:
    def __init__(self, world):
        self.world = world
        self.infection = world.infection

    def infect(self, country):
        probability = min((70 * country.population) /
                          (country.population * len(country.connections)), 1)
        if random() < probability:
            country.set_state('Infected')
            country.infect_people(1)
            return True
        return False

    def apply_damage(self, country):
        # Original method: too damn slow
        # for person in range(country.num_infected):
        #    num = randint(0, 6)
        #    num *= self.infection.contagiousness
        #    if country.masks_provided:
        #        num *= 0.3
        #    country.infect_people(round(num))
        num = randint(0, 6)
        num *= country.num_infected
        num *= self.infection.contagiousness
        if country.masks_provided:
            num *= 0.3
        country.infect_people(int(num))

        if country.num_infected:
            mean = 0
            if country.num_infected < 10:
                num_people = int(country.num_infected)
            else:
                num_people = int(max(0.000001 * country.num_infected, 10))
            #print(country.name, country.num_infected, country.population)
            for person in range(num_people):
                probability = self.calculate_probability_of_death()
                mean += int(random() < probability)
            mean /= num_people
            # print(mean)
            num_people_to_kill = mean * country.num_infected
            country.kill_people(int(num_people_to_kill))

    def calculate_probability_of_death(self):
        probability = min((max(0.2, (self.world.time ** 2) / 100000)) *
                          self.infection.mortality, 1)
        return probability

'''
Comentario:
El tiempo que la función apply_damage() se demora aumenta considerablemente a
medida que los días pasan. Esto se debe a que el for loop recorre un rango muy
grande, pues estamos realizando cálculos cada persona (uff!). Para
reducir el tiempo de ejecución se puede verificar una vez si el valor aleatorio
es menor que la probabilidad y eso es valido para todas las personas
infectadas. Esta alternativa apareció en una issue.

Para el cálculo de las muertes de reduce la cantidad de iteraciones a un
porcentaje del número de infectados. Luego se saca el promedio
'''