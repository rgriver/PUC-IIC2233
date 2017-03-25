from users import *
from resources import *
from fires import *
from forecasts import *


class DataCollection:
    def __init__(self):
        self.users = Users('usuarios.csv')
        self.resources = Resources('recursos.csv')
        self.fires = Fires('incendios.csv')
        self.forecasts = Forecasts('meteorologia.csv')

    def get_users_database(self):
        return self.users

    def get_resources_database(self):
        return self.resources

    def get_fires_database(self):
        return self.fires

    def get_forecasts_database(self):
        return self.forecasts
