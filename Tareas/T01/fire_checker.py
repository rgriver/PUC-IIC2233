import os

class FireChecker:
    def __init__(self, fires, login):
        self.resource_id = None
        self.fires = fires
        self.fires_list = []
        self.login = login

    def check(self):
        self.fires_list = []
        self.resource_id = self.login.resource_id
        path = 'Reportes Estrategias de Extinción'
        if os.path.exists(path):
            for file in os.listdir(path):
                file = os.path.join(path, file)
                f = open(file, 'r')
                fire_id = next(f).strip()
                while True:
                    line = next(f, None)
                    if line is None:
                        break
                    line = line.strip()
                    line = line.split(',')
                    if self.resource_id == line[0]:
                        self.fires_list.append(fire_id)
                        break

        fire_tuple = ('ID: ', 'Latitude: ', 'Longitude: ', 'Power: ',
                      'Start date: ')
        fire_str = ''
        for fire in self.fires_list:
            line = self.fires.get_line(fire)
            for i, j in zip(fire_tuple, line):
                fire_str += i + j + '\n'
            fire_str += '---------------------------------------- \n\n'
        return fire_str
