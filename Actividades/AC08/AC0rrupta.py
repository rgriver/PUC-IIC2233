__author__ = "cotehidalgov"
__coauthor__ = "Diego Andai"
# -*- coding: utf-8 -*-
import random

###############################################################################
#Solo puedes escribir código aquí, cualquier modificación fuera de las lineas
#será penalizada con nota 1.0


class MetaPerson(type):
    def __new__(mcs, name, bases, dic):
        if name == 'Chef':
            bases = (Person,)

            if 'cook' not in dic.keys():
                def cook(self):
                    plate = Plate()
                    self.choose_drink(plate)
                    self.choose_food(plate)
                    return plate
                dic['cook'] = cook

            dic['restaurant_name'] = None

        if name == 'Client':
            bases = (Person,)

            if 'eat' not in dic.keys():
                def eat(self, plate):
                    if isinstance(plate.food, Food) and isinstance(plate.drink, Food):
                        print("Mi plato tiene dos comidas")
                    if isinstance(plate.food, Drink) and isinstance(plate.drink, Drink):
                        print("Mi plato tiene dos bebidas")
                    else:
                        if plate.food._quality + plate.drink._quality  > 50:
                            print("Que delicia")
                        else:
                            print("Esto no es digno de mi paladar")

            dic['eat'] = eat

        return super().__new__(mcs, name, bases, dic)


class MetaRestaurant(type):
    restaurants = []

    def __new__(mcs, name, bases, dic):

        def llega_cliente(self, client):
            if isinstance(client, Client):
                self.clients.append(client)

        def cliente_se_va(self, name):
            client = None
            for c in self.clients:
                if c.name == name:
                    client = c
            if client:
                self.clients.remove(client)

        dic['llega_cliente'] = llega_cliente
        dic['cliente_se_va'] = cliente_se_va

        old_start = dic['start']

        def new_start(self):
            if len(self.clients) > 0:
                old_start(self)
            else:
                print(self.name, 'no tiene clientes, que pena')

        dic['start'] = new_start

        return super().__new__(mcs, name, bases, dic)

    def __call__(cls, *args, **kwargs):

        if len(args) == 1:
            name = args[0]
            chefs = []
            clients = []
        elif len(args) == 2:
            name = args[0]
            chefs = args[1]
            clients = []
        else:
            name = args[0]
            chefs = args[1]
            clients = args[2]

        # MetaRestaurant.names[args[0]] = args[1]

        for restaurant in MetaRestaurant.restaurants:
            for chef in restaurant.chefs:
                temp = []
                if chef in chefs:
                    temp.append(chef)
            for chef in temp:
                if len(restaurant.chefs) > 1:
                    restaurant.chefs.remove(chef)
                    chefs.restaurant_name = name

        restaurant = super().__call__(name, chefs, clients)
        print('Instanciación exitosa')
        for chef in restaurant.chefs:
            print('Chef: ' + chef.name)
        MetaRestaurant.restaurants.append(restaurant)
        return restaurant



###############################################################################
#De aquí para abajo no puedes cambiar ABSOLUTAMENTE NADA


class Person:
    def __init__(self, name):
        self.name = name


class Food:
    def __init__(self, ingredients):
        self._quality = random.randint(50, 200)
        self.preparation_time = 0
        self.ingredients = ingredients


    @property
    def quality(self):
        return self._quality * random.random()


class Drink:
    def __init__(self):
        self._quality = random.randint(5, 15)

    @property
    def quality(self):
        return self._quality * random.random()


class Restaurant(metaclass = MetaRestaurant):
    def __init__(self, name, chefs, clients):
        self.name = name
        self.chefs = chefs
        self.clients = clients


    def start(self):
        for i in range(1):  # Se hace el estudio por 5 dias
            print("----- Día {} -----".format(i + 1))
            plates = []
            for chef in self.chefs:
                for j in range(3):  # Cada chef cocina 3 platos
                    plates.append(chef.cook())  # Retorna platos de comida y bebida

            for client in self.clients:
                for plate in plates:
                    client.eat(plate)


class Pizza(Food):
    def __init__(self, ingredients):
        super(Pizza, self).__init__(ingredients)
        self.preparation_time = random.randint(5, 100)


class Salad(Food):
    def __init__(self, ingredients):
        super(Salad, self).__init__(ingredients)
        self.preparation_time = random.randint(5, 60)


class Coke(Drink):
    def __init__(self):
        super(Coke, self).__init__()
        self._quality -= 5


class Juice(Drink):
    def __init__(self):
        super(Juice, self).__init__()
        self._quality += 5


class Plate:
    def __init__(self):
        self.food = None
        self.drink = None


class Chef(Pizza, metaclass=MetaPerson):
    def __init__(self, name):
        super(Chef, self).__init__(name)

    def choose_food(self, plate):
        food_choice = random.randint(0, 1)
        ingredients = []
        if food_choice == 0:
            for i in range(3):
                ingredients.append(random.choice(["pepperoni", "piña", "cebolla", "tomate", "jamón", "pollo"]))
            plate.food = Pizza(ingredients)
        else:
            for i in range(2):
                ingredients.append(random.choice(["crutones", "espinaca", "manzana", "zanahoria", "palta"]))
            plate.food = Salad(ingredients)

    def choose_drink(self, plate):
        drink_choice = random.randint(0, 1)
        if drink_choice == 0:
            plate.drink = Coke()
        else:
            plate.drink = Juice()


class Client(Pizza, metaclass=MetaPerson):
    def __init__(self, name):
        super(Client, self).__init__(name)


if __name__ == '__main__':

    chefs = [Chef("Enzo"), Chef("Nacho"), Chef("Diego")]
    clients = [Client("Bastian"), Client("Flori"),
                Client("Rodolfo"), Client("Felipe")]
    McDollars = Restaurant("Mc", chefs, clients)

    BurgerPimp = Restaurant("BK")

    KFK = Restaurant("KFK", [Chef("Enzo")])

    McDollars.start()
    KFK.start()
