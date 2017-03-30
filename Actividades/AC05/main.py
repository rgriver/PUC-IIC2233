class CustomException(Exception):
    def __init__(self, bin_word):
        self.word = ''
        self.bin_word = bin_word

    def fix_bin(self):
        fixed_word = self.bin_word[::-1]
        return fixed_word


class Descifrador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.suma=0
        self.a_detected = False
        with open(self.nombre, "r") as self.archivo:
            lineas = self.archivo.readlines()
            self.codigo = ''
            self.texto = "".join(lineas).replace('\n', '')
            i = 0

    def lectura_archivo(self):
        with open(self.nombre, "r") as archivo:
            lineas = archivo.readlines()
            self.codigo = ''
            texto = "".join(lineas).replace('\n', '')
            for caracter in texto:
                self.codigo += caracter
            return self.codigo

    def elimina_incorrectos(self):
        lista=self.codigo.split(" ")
        self.codigo=''
        for i in lista:
            try:
                if i > 'a':
                    self.a_detected = True
                    raise CustomException(i[1:])
                elif self.a_detected:
                    raise CustomException(i)
                if len(i) < 6 or len(i) > 7:
                    pass
                else:
                    self.codigo+=' '+i
            except CustomException as err:
                new_bin = err.fix_bin()
                if len(new_bin) == 7:
                    self.codigo += ' ' + err.fix_bin()
        return self.codigo

    def cambiar_binario(self, binario):
        lista = binario.split(' ')
        texto = []
        for x in lista[1:]:
            texto.append(chr(int(x, 2)))
        return texto

    def limpiador(self, lista):
        i = -1
        string = ''
        while i < len(lista):
            i += 1
            try:
                if '$' != lista[i]:
                    string += lista[i]
                    raise CustomException()
            except CustomException as e:
                i = 0
        return string

if __name__ == "__main__":
    try:
        des = Descifrador('mensaje_marciano.txt')
        codigo= des.lectura_archivo()
        codigo=des.elimina_incorrectos()
        lista = des.cambiar_binario(des.codigo)
        texto = des.limpiador(lista)
    except Exception as err:
        print('Esto no debiese imprimirse')