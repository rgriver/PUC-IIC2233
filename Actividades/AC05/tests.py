import unittest
from main import CustomException, Descifrador

class TestearFormato(unittest.TestCase):
    def setUp(self):
        self.archivo = open('mensaje_marcianito.txt', 'r')

    def test_archivo(self):
        lineas = self.archivo.readlines()
        self.codigo = ''
        self.texto = "".join(lineas).replace('\n', '')
        num_elements = len(self.texto)
        self.assertEqual(num_elements, 403)
        char_sum = sum([int(i, 2) for i in self.texto])
        self.assertEqual(char_sum, 253)


class TestearMensaje(unittest.TestCase):
    def setUp(self):
        self.des = Descifrador('mensaje_marciano.txt')

    def test_incorrectos(self):
        codigo = self.des.elimina_incorrectos()
        for char in codigo:
            length = len(char)
            self.assertEqual(length, 7)

    def test_caracteres(self):
        texto = self.des.limpiador()
        for element in texto:
            self.assertEqual(element,'$')

    def test_codificacion(self):
        codigo = self.des.elimina_incorrectos()
        for bin_word in codigo:
            for char in bin_word:
                self.assertEqual(char,)