from database import *

class AirportsDatabase(Database):
    def __init__(self, filename):
        super(AirportsDatabase, self).__init__(filename)
