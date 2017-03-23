# PRIMERA PARTE: Estructura basica
class Nodo:
    def __init__(self, valor=None):
        self.siguiente = None
        self.valor = valor

class Lista:
    def __init__(self, *args):
        self.cola = None
        self.cabeza = None
        for arg in args:
            self.append(arg)

    def append(self, valor):
        if not self.cabeza:
            self.cabeza = Nodo(valor)
            self.cola = self.cabeza
        else:
            self.cola.siguiente = Nodo(valor)
            self.cola = self.cola.siguiente

    def __getitem__(self, index):
        nodo = self.cabeza
        for i in range(index):
            if nodo:
                nodo = nodo.siguiente
            else:
                raise IndexError
        if not nodo:
            raise IndexError
        else:
            return nodo.valor

    def __in__(self, valor):
        for elemento in self:
            if elemento == valor:
                return True
        return False

    def __repr__(self):
        nodo = self.cabeza
        s = "["
        if nodo:
            s += str(nodo.valor) + ", "
        else:
            return "[]"
        while nodo.siguiente:
            nodo = nodo.siguiente
            s += str(nodo.valor) + ", "
        return s.strip(", ") + "]"



# SEGUNDA PARTE: Clase Isla
class Isla:
    def __init__(self, nombre):
        self.nombre = nombre
        self.conexiones = Lista()

    def __repr__(self):
        return self.nombre


# TERCERA PARTE: Clase Archipielago
class Archipielago:
    def __init__(self,archivo):
        self.islas = Lista()
        self.archivo = archivo

    def __repr__(self):
        self.construir(self.archivo)
        s = ""
        for isla in self.islas:
            s += "    {}  conectada con: {} \n".format(isla.nombre,isla.conexiones)
        return s.strip()


    def agregar_isla(self, nombre):
        for i in self.islas:
            if nombre == i.nombre:
                return None
        self.islas.append(Isla(nombre))

    def conectadas(self, nombre_origen, nombre_destino):
        isla_origen = None
        for i in self.islas:
            if nombre_origen == i.nombre:
                isla_origen = i
                break
        for i in isla_origen.conexiones:
            if nombre_destino == i.nombre:
                return True
        return False

    def agregar_conexion(self, nombre_origen, nombre_destino):
        isla_origen = None
        isla_destino =  None
        for i in self.islas:
            if nombre_origen == i.nombre:
                isla_origen = i
            if nombre_destino == i.nombre:
                isla_destino = i
        isla_origen.conexiones.append(isla_destino)

    def construir(self,archivo):
        f = open(archivo)
        for l in f:
            l = l.strip()
            nombre1, nombre2 = l.split(',')
            self.agregar_isla(nombre1)
            self.agregar_isla(nombre2)
            if not self.conectadas(nombre1,nombre2):
                self.agregar_conexion(nombre1,nombre2)

    def propagacion(self, nombre_origen):
        self.construir(self.archivo)
        lista_propagacion = Lista()
        for i in self.islas:
            if nombre_origen == i.nombre:
                lista_propagacion.append(i.conexiones)
                for a in i.conexiones:
                    self.propagacion(a)

        return lista_propagacion





if __name__ == '__main__':
    pass
    # No modificar desde esta linea
    # (puedes comentar lo que no este funcionando aun)
    arch = Archipielago("mapa.txt") # Instancia y construye
    #print(arch) # Imprime el Archipielago de una forma que se pueda entender
    print(arch.propagacion("Perresus"))
    #print(arch.propagacion("Pasesterot"))
    #print(arch.propagacion("Cartonat"))
    #print(arch.propagacion("Womeston"))






