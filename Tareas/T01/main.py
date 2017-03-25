import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from users import *
from login import *
from window import *
from user_date import *
from data_collection import *


if __name__ == '__main__':
    '''
    app = QApplication(sys.argv)
    users = Users('usuarios.csv')
    login = Login(users)
    date = Date(login)
    window = Window(login, date, users)
    login.accepted.connect(date.show)
    login.accepted.connect(window.set_menu)
    date.accepted.connect(window.show)
    app.exit(app.exec_())

    '''
    app = QApplication(sys.argv)
    data_collection = DataCollection()
    login = Login(data_collection.get_users_database())
    user_date = UserDate(login)
    window = Window(login, user_date, data_collection)
    login.accepted.connect(user_date.show)
    login.accepted.connect(window.set_menu)
    user_date.accepted.connect(window.show)
    app.exit(app.exec_())

