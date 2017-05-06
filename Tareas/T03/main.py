from gui.Gui import MyWindow
from PyQt5 import QtWidgets
import sys
import interpretation
import errors
import core
import data_reading


class T03Window(MyWindow):
    def __init__(self):
        super().__init__()
        errors.show = self.add_answer
        core.show = self.add_answer

    def process_consult(self, querry_array):
        # Legal use of for loop
        for query in querry_array:
            try:
                if not query:
                    raise ValueError("Empty query.\n")
                errors.command = interpretation.command_to_str(query)
                if interpretation.validate_command(query):
                    value = interpretation.simplify(query)
                    if value is not None:
                        data_reading.output.append(str(value) + '\n')
                        self.add_answer(str(value) + '\n')
                    else:
                        data_reading.output.append(query[0] + '\n')
            except TypeError as e:
                errors.RqlError(str(e))
                continue
            except ValueError as e:
                errors.RqlError(str(e))
                continue
            except FileNotFoundError as e:
                errors.RqlError(str(e))
                continue
            except errors.UndefinedFunction:
                continue
            except errors.ReservedName:
                continue
            except errors.NoArguments:
                continue
            except errors.ImpossibleProcessing:
                continue
            except errors.MathError:
                continue
            except errors.ArgumentError:
                continue

    def save_file(self, querry_array):
        # Crea un archivo con la solucion. NO muestra los graficos!!
        data_reading.write_data()
        # print(querry_array)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = T03Window()
    sys.exit(app.exec_())
