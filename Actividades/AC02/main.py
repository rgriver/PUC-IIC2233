from random import randint
from abc import ABC, abstractmethod


class Plate:
    def __init__(self, food, drink):
        self.food = food
        self.drink = drink


class Food:
    def __init__(self, ingredients):
        self.ingredients = ingredients
        self.time = None
        self.quality = randint(50, 200)

    def check_time(self):
        if self.time >= 30:
            self.quality -= 30

    def get_quality(self):
        return self.quality


class Pizza(Food):
    def __init__(self, ingredients):
        super(Pizza, self).__init__(ingredients)
        self.time = randint(20, 100)

    def check_ingredients(self):
        if 'pepperoni' in self.ingredients:
            self.quality += 50
        elif 'pineapple' in self.ingredients:
            self.quality -= 50


class Salad(Food):
    def __init__(self, ingredients):
        super(Salad, self).__init__(ingredients)
        self.time = randint(5, 60)

    def check_ingredients(self):
        if 'crouton' in self.ingredients:
            self.quality += 20
        elif 'apple' in self.ingredients:
            self.quality -= 20


class Drink:
    def __init__(self):
        self.quality = randint(50, 150)

    def get_quality(self):
        return self.quality


class Juice(Drink):
    def __init__(self):
        super(Juice, self).__init__()
        self.quality += 30


class Soda(Drink):
    def __init__(self):
        super(Soda, self).__init__()
        self.quality -= 30


class Person:
    def __init__(self, name):
        self.name = name


class Chef(Person):
    def __init__(self, name):
        super(Chef, self).__init__(name)
        self.plate = None

    def cook(self):

        food_choice = randint(0, 1)
        drink_choice = randint(0, 1)

        if food_choice:
            ingredients = ['cheese', 'sauce']
            extra_ingredients = ['pepperoni', 'pineapple', 'onion', 'tomato', 'ham', 'chicken']
            for i in range(3):
                ingredients.append(extra_ingredients[randint(0, 5)])
            food = Pizza(ingredients)
        else:
            ingredients = ['lettuce']
            extra_ingredients = ['crouton', 'spinach', 'apple', 'carrot']
            for i in range(2):
                ingredients.append(extra_ingredients[randint(0, 3)])
            food = Salad(ingredients)

        if drink_choice:
            drink = Juice()
        else:
            drink = Soda()

        self.plate = Plate(food, drink)
        return self.plate


class Client(Person):
    def __init__(self, name, personality):
        super(Client, self).__init__(name)
        self.personality = personality

    def eat(self, plate):
        print(self.name + ': ', end='')
        self.personality.react(plate)


class Personality(ABC):
    @abstractmethod
    def im_happy(self):
        pass

    def im_mad(self):
        pass

    def react(self, plate):
        food = plate.food
        drink = plate.drink
        food.check_time()
        food.check_ingredients()
        quality = (food.get_quality() + drink.get_quality())/2
        if quality >= 100:
            self.im_happy()
        else:
            self.im_mad()


class Cool(Personality):
    def __init__(self):
        super(Cool, self).__init__()

    def im_happy(self):
        print('Yumi! Que rico')

    def im_mad(self):
        print('Preguntaré si puedo cambiar el plato')


class Hater(Personality):
    def __init__(self):
        super(Hater, self).__init__()

    def im_happy(self):
        print('No está malo, pero igual prefiero Pizza x2')

    def im_mad(self):
        print('Nunca mas vendré a Daddy Juan\'s')


class Restaurant:
    def __init__(self, chefs, clients):
        self.chefs = chefs
        self.clients = clients

    def start(self):
        for i in range(3):
            print('----- Día {} -----'.format(i + 1))
            plates = []
            for chef in self.chefs:
                for j in range(3):
                    plates.append(chef.cook())

            for client in self.clients:
                for plate in plates:
                    client.eat(plate)

if __name__ == '__main__':
    chefs = [Chef('Cote'), Chef('Joaquin'), Chef('Andres')]
    clients = [Client('Bastian', Hater()), Client('Flori', Cool()), Client('Antonio', Hater()), Client('Felipe', Cool())]

    restaurant = Restaurant(chefs, clients)
    restaurant.start()
