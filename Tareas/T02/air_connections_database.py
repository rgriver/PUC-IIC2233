from database import *


class AirConnectionsDatabase(Database):
    def __init__(self, filename):
        super(AirConnectionsDatabase, self).__init__(filename)