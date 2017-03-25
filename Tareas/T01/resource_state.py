import os
from date_time import *
from optimizer import *


class ResourceState:
    def __init__(self, date, resources, fires, resource_id):
        self.lat = None
        self.lon = None
        self.distance = None
        self.date = date
        self.start = DateTime()
        self.end = DateTime()
        self.resources = resources
        self.fires = fires
        self.fire_id = None
        self.resource_id = resource_id
        self.status = 'Stand By'

    def update_state(self):
        path = 'Reportes Estrategias de Extinción'
        if os.path.exists(path):
            for file in os.listdir(path):
                file = os.path.join(path, file)
                f = open(file, 'r')
                self.fire_id = next(f).strip()
                while True:
                    line = next(f, None)
                    if line is None:
                        break
                    line = line.strip()
                    line = line.split(',')
                    if self.resource_id == line[0]:
                        if self.to_fire(line):
                            self.status = 'To Fire'
                            self.set_coordinates()
                            return 1
                        elif self.working(line):
                            self.status = 'Working'
                            self.set_coordinates()
                            return 2
                        elif self.to_headquarters(line):
                            self.status = 'To Headquarters'
                            self.set_coordinates()
                            return 3
                        elif self.sleeping(line):
                            self.status = 'Resting'
                            self.set_coordinates()
                            return 4
        self.status = 'Stand By'
        if self.resource_id:
            self.lat = self.resources.get_line(self.resource_id)[2]
            self.lon = self.resources.get_line(self.resource_id)[3]
        return 0

    def to_fire(self, line):
        if line[1] <= self.date.get_formatted_date_time() < line[2]:
            self.start.set_formatted_date_time(line[1])
            self.end.set_formatted_date_time(line[2])
            return True
        return False

    def working(self, line):
        if line[2] <= self.date.get_formatted_date_time() < line[3]:
            self.start.set_formatted_date_time(line[2])
            self.end.set_formatted_date_time(line[3])
            return True
        return False

    def to_headquarters(self, line):
        if line[3] <= self.date.get_formatted_date_time() < line[4]:
            self.start.set_formatted_date_time(line[3])
            self.end.set_formatted_date_time(line[4])
            print(self.start.get_formatted_date_time(), self.end.get_formatted_date_time())
            return True
        return False

    def sleeping(self, line):
        if line[4] <= self.date.get_formatted_date_time() <= line[5]:
            self.start.set_formatted_date_time(line[4])
            self.end.set_formatted_date_time(line[5])
            return True
        return False

    def set_coordinates(self):
        fire_line = self.fires.get_line(self.fire_id)
        resource_line = self.resources.get_line(self.resource_id)
        fire_lat = float(fire_line[1])
        fire_lon = float(fire_line[2])
        resource_lat = float(resource_line[2])
        resource_lon = float(resource_line[3])
        self.lat = (fire_lat - resource_lat) / (self.end - self.start)
        self.lat *= self.date - self.start
        self.lat += resource_lat
        self.lon = (fire_lon - resource_lon) / (self.end - self.start)
        self.lon *= self.date - self.start
        self.lon += resource_lon
        self.distance = Optimizer.calculate_distance(self.lat, self.lon,
                                                     fire_lat, fire_lon)

    def get_state_string(self):
        state_str = 'Status: ' + self.status + '\n'
        state_str += 'Current location: ' + str(self.lat) + ', ' + \
                     str(self.lon) + '\n'
        if self.status == 'To Fire' or self.status == 'To Headquarters':
            state_str += 'Distance to target: ' + str(self.distance) + '\n'
        if self.status == 'Working':
            state_str += 'Time worked: ' + ResourceState.secs_to_format(
                self.date - self.start) + '\n'
            state_str += 'Remaining time: ' + ResourceState.secs_to_format(
                self.end - self.date) + '\n'
        return state_str

    @staticmethod
    def secs_to_format(time):
        time = int(time)
        hour = int(time / 3600)
        time_str = ''
        if hour > 0:
            time %= 3600
            time_str += '{} hour{}, '.format(hour, '' if hour == 1 else 's')
        minute = int(time / 60)
        if minute > 0:
            time %= 60
            time_str += '{} minute{}, '.format(minute, '' if minute == 1 else
                                               's')
        second = time
        if second > 0:
            time_str += '{} second{}, '.format(second, '' if second == 1 else
                                               's')
        return time_str

