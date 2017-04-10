from database import *


class PopulationDatabase(Database):
    def __init__(self, filename):
        super(PopulationDatabase, self).__init__(filename)
