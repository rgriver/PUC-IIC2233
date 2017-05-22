import sys
from PyQt5.QtWidgets import QApplication
from view import View
from simulator import Simulator

if __name__ == '__main__':
    app = QApplication(sys.argv)
    simulator = Simulator()
    view = View(simulator)
    #simulator.run()
    app.exit(app.exec_())
