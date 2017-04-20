__author__ = 'Ignacio Castaneda, Diego Iruretagoyena, Ivania Donoso, CPB'

import random
from datetime import datetime


"""
Escriba sus decoradores y funciones auxiliares en este espacio.
"""

def existe_cuenta(cuentas, cuenta):
    if cuenta in cuentas:
        return True
    return False

def verificar_fondos(cuenta, monto):
    if cuenta.saldo - monto >= 0:
        return True
    return False

def validar_clave(cuenta, clave):
    if cuenta.clave == clave:
        return True
    return False

def verificar_limite_inversion(cuenta, monto):
    if cuenta.inversiones + monto <= 10000000:
        return True
    return False

def verificar_disponibilidad(cuentas, numero):
    numeros = [cuenta for cuenta in cuentas]
    if numero in numeros:
        while True:
            new_numero = str(random.randint(0, 10000))
            if new_numero not in numeros:
                break
        return new_numero
    else:
        return numero

def verificar_formato_clave(clave):
    if len(clave) == 4:
        return True
    return False

def verificar_formato_rut(rut):
    temp_rut = rut[:-2]
    if '-' in temp_rut:
        return False

    if temp_rut.isdigit():
        return True
    else:
        return False

# DECORADORES

def verificar_transferencia(f):
    def new_transferir(self, origen, destino, monto, clave):
        val_origen = origen in self.cuentas
        if val_origen is False:
            raise Exception('No existe la cuenta de origen')
        val_destino = destino in self.cuentas
        if val_destino is False:
            raise Exception('No existe la cuenta de destino')
        fondos = False
        if val_origen:
            fondos = self.cuentas[origen].saldo - monto >= 0
            if fondos is False:
                raise Exception('No hay fondos')
        clave_ok = clave == self.cuentas[origen].clave
        if clave_ok is False:
            raise Exception('Clave incorrecta')
        if val_origen and val_destino and fondos and clave_ok:
            f(self, origen, destino, monto, clave)
            print('Transferencia realizada')

    return new_transferir

def verificar_inversion(f):
    def new_invertir(self, cuenta, monto, clave):
        cuenta_ok = existe_cuenta(self.cuentas, cuenta)
        saldo_ok = clave_ok = limite_ok = False
        if cuenta_ok:
            saldo_ok = verificar_fondos(self.cuentas[cuenta], monto)
            if saldo_ok is False:
                raise Exception('No hay fondos suficientes')
            clave_ok = validar_clave(self.cuentas[cuenta], clave)
            if clave_ok is False:
                raise Exception('La clave es incorrecta')
            limite_ok = verificar_limite_inversion(self.cuentas[cuenta, monto])
            if limite_ok is False:
                raise Exception('Supera el límite de inversión')
        if cuenta_ok and saldo_ok and clave_ok and limite_ok:
            f(self, cuenta, monto, clave)
            print('Inversión realizada')

    return new_invertir


def verificar_cuenta(f):
    def new_crear_cuenta(self, nombre, rut, clave, numero, saldo_inicial=0):
        numero_final = verificar_disponibilidad(self.cuentas, numero)
        clave_ok = verificar_formato_clave(clave)
        if clave_ok is False:
            raise Exception('Clave no cumple con el formato')
        rut_ok = verificar_formato_rut(rut)
        if rut_ok is False:
            raise Exception('RUT no cumple con el formato')
        if clave_ok and rut_ok:
            f(self, nombre, rut, clave, numero_final, saldo_inicial)
            print('Cuenta creada correctamente')
    return new_crear_cuenta


def verificar_saldo(f):
    def new_saldo(self, numero_cuenta):
        cuenta_ok = existe_cuenta(self.cuentas, numero_cuenta)
        if cuenta_ok is False:
            raise Exception('La cuenta no existe')
        if cuenta_ok:
            saldo = f(self, numero_cuenta)/5
            return saldo
    return new_saldo


def log(f, filename):
    name = f.__name__
    def new_atribute(*args):
        with open(filename, 'w') as file:
            if name == 'saldo':
                file.write('Saldo\n')
            elif name == 'crear_cuenta\n':
                file.write('Creación de cuenta\n')
            elif name == 'transferir':
                file.write('Transferencia\n')
            elif name == 'invertir':
                file.write('Nueva inversión')
        f(*args)
    return new_atribute






"""
No pueden modificar nada más abajo, excepto para agregar los decoradores a las
funciones/clases.
"""

class Banco:
    def __init__(self, nombre, cuentas=None):
        self.nombre = nombre
        self.cuentas = cuentas if cuentas is not None else dict()

    @verificar_saldo
    def saldo(self, numero_cuenta):
        # Da un saldo incorrecto
        return self.cuentas[numero_cuenta].saldo * 5

    @verificar_transferencia
    def transferir(self, origen, destino, monto, clave):
        # No verifica que la clave sea correcta, no verifica que las cuentas
        # existan
        self.cuentas[origen].saldo -= monto
        self.cuentas[destino].saldo += monto

    @verificar_cuenta
    def crear_cuenta(self, nombre, rut, clave, numero, saldo_inicial=0):
        # No verifica que el número de cuenta no exista
        cuenta = Cuenta(nombre, rut, clave, numero, saldo_inicial)
        self.cuentas[numero] = cuenta

    @verificar_inversion
    def invertir(self, cuenta, monto, clave):
        # No verifica que la clave sea correcta ni que el monto de las
        # inversiones sea el máximo
        self.cuentas[cuenta].saldo -= monto
        self.cuentas[cuenta].inversiones += monto

    def __str__(self):
        return self.nombre

    def __repr__(self):
        datos = ''

        for cta in self.cuentas.values():
            datos += '{}\n'.format(str(cta))

        return datos

    @staticmethod
    def crear_numero():
        return int(random.random() * 100)


class Cuenta:
    def __init__(self, nombre, rut, clave, numero, saldo_inicial=0):
        self.numero = numero
        self.nombre = nombre
        self.rut = rut
        self.clave = clave
        self.saldo = saldo_inicial
        self.inversiones = 0

    def __repr__(self):
        return "{} / {} / {} / {}".format(self.numero, self.nombre, self.saldo,
                                          self.inversiones)


if __name__ == '__main__':
    bco = Banco("Santander")
    bco.crear_cuenta("Mavrakis", "4057496-7", "1234", bco.crear_numero())
    bco.crear_cuenta("Ignacio", "19401259-4", "1234", 1, 24500)
    bco.crear_cuenta("Diego", "19234023-3", "1234", 2, 13000)
    bco.crear_cuenta("Juan", "19231233--3", "1234", bco.crear_numero())

    print(repr(bco))
    print()

    """
    Estos son solo algunos casos de pruebas sugeridos. Sientase libre de agregar
    las pruebas que estime necesaria para comprobar el funcionamiento de su
    solucion.
    """
    try:
        print(bco.saldo(10))
    except AssertionError as error:
        print('Error: ', error)

    try:
        print(bco.saldo(1))
    except AssertionError as error:
        print('Error: ', error)

    try:
        bco.transferir(1, 2, 5000, "1234")
    except AssertionError as msg:
        print('Error: ', msg)

    try:
        bco.transferir(1, 2, 5000, "4321")
    except AssertionError as msg:
        print('Error: ', msg)

    print(repr(bco))
    print()

    try:
        bco.invertir(2, 200000, "1234")
    except AssertionError as error:
        print('Error: ', error)
    print(repr(bco))

    try:
        bco.invertir(2, 200000, "4321")
    except AssertionError as error:
        print('Error: ', error)
    print(repr(bco))
