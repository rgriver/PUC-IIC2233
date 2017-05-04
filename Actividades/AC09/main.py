from collections import deque
from random import choice
from random import expovariate, randint, random


class Simulation:
    def __init__(self):
        self.simulation_time = 0
        self.walking_death = 0
        self.car_death = 0
        self.tsunami = 0
        self.power = 0
        self.next_quake()
        self.walkers = []
        self.cars = []
        self.delta = 0
        for i in range(75):
            self.walkers.append(Person())
        for i in range(25):
            self.cars.append(Car())

    def next_quake(self):
        self.delta = expovariate(1/randint(4, 10))
        self.simulation_time += self.delta
        intensity = random()
        if intensity > 0.7:
            self.walking_death = 0.3
            self.car_death = 0.6
            if random() > 0.3:
                self.power = randint(3, 8)
            else:
                self.power = 0
        else:
            self.walking_death = 0.1
            self.car_death = 0.15
            self.power = 0

    def kill(self):
        dead_walkers = []
        dead_cars = []
        for walker in self.walkers:
            walker.update(self.delta)
            if walker.position < 100:
                if random() < self.walking_death:
                    dead_walkers.append(walker)
        for walker in dead_walkers:
            self.walkers.remove(walker)

        for car in self.cars:
            car.update(self.delta)
            if car.position < 100:
                if random() < self.car_death:
                    dead_cars.append(car)
        for car in dead_cars:
            self.cars.remove(car)

        if self.power > 0:

            dead_walkers = []
            dead_cars = []

            tsunami_position = randint(0, 100)
            start = tsunami_position - 4 * self.power
            end = tsunami_position + 4 * self.power

            for walker in self.walkers:
                if walker.position < 100:
                    if end < walker.position < start:
                        if random() < self.walking_death:
                            dead_walkers.append(walker)
            for walker in dead_walkers:
                self.walkers.remove(walker)

            for car in self.cars:
                if car.position < 100:
                    if end < car.position < start:
                        if random() < self.car_death:
                            dead_cars.append(car)
            for car in dead_cars:
                self.cars.remove(car)

    def add_to_car(self):
        chosen_walkers = []

        for car in self.cars:
            for walker in self.walkers:
                if walker.position == car.position and car.capacity > 0:
                    if random() < car.stop_probability:
                        walker.speed = car.speed
                        walker.car = True
                        chosen_walkers.append(walker)
                        car.capacity -= 1

        for walker in chosen_walkers:
            self.walkers.remove(walker)

    def run(self):
        car_ok = all(map(lambda x: x.position > 100, self.cars))
        walker_ok = all(map(lambda x: x.position > 100, self.walkers))
        while self.simulation_time < 200 or (car_ok and walker_ok):
            self.next_quake()
            self.kill()
            self.add_to_car()

        counter_5 = 0
        counter_8 = 0
        for car in self.cars:
            if car.init_capacity == 5:
                counter_5 += 5 - min(car.capacity, 0)
            else:
                counter_8 += 8 - min(car.capacity, 0)

        count_walkers = len([walker for walker in self.walkers if walker.position >= 100])
        count_generoso = len([car for car in self.cars if car.stop_probability == 0.6 and car.position >= 100])
        count_egoista = len([car for car in self.cars if car.stop_probability == 0.3 and car.position >= 100])

        print('Numero de llegados a la base por auto:', counter_5)
        print('Numero de llegados a la base por camioneta:', counter_8)
        print('Numero de llegados a la base a pie: ', count_walkers)
        print('Numero de llegados a la base que son generosos: ', count_generoso)
        print('Numero de llegados a la base que son egoistas: ', count_egoista)
        print('\n')

        self.__init__()

class Person:
    def __init__(self):
        self.speed = randint(5, 8)
        self.auto = False
        self.position = randint(0, 60)

    def update(self, time):
        self.position += self.speed * time


class Car:
    def __init__(self):
        self.speed = randint(12, 20)
        self.passengers = []
        car_choice = randint(0, 1)
        if car_choice == 1:
            self.capacity = 4
            self.init_capacity = 5
        else:
            self.capacity = 7  # El conductor no cuenta
            self.init_capacity = 8
        personality_choice = randint(0, 1)
        if personality_choice == 1:
            self.stop_probability = 0.3
        else:
            self.stop_probability = 0.6
        self.position = randint(0, 60)

    def update(self, time):
        self.position += self.speed * time


if __name__ == '__main__':
    sim = Simulation()
    for i in range(10):
        sim.run()
