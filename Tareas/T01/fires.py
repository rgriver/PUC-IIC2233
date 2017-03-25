from database import *

class Fires(Database):
    def __init__(self, filename):
        self.filename = filename

    def set_fire(self, latitude, longitude, power, start):
        file = open(self.filename, 'r+')
        for line in file:
            pass
        line = line.split(',')
        last_id = int(line[0])
        new_id = str(last_id + 1)
        file.write('\n' + ','.join([new_id, latitude, longitude, power, start]))
