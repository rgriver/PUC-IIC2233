from math import *

class ResourceOptimizer:
    def __init__(self, fire_id, resources, forecasts):
        self.fire_id = fire_id
        self.resources = resources
        self.forecasts = forecasts
        self.date = DateTime()

    def optimize(self):
        fire_line = self.fire.get_line(self.fire_id)
        start = fire_line[4]
        start = start.replace('-', ' ')
        start = start.replace(':', ' ')
        start = start.split(' ')
        start = [int(x) for x in start]
        points = fire_line
        y, mo, d, h, mi, s = start
        self.date.set_date_time(y, mo, d, h, mi, s)
        seconds = 60
        while points > 0:
            self.date.add_seconds(seconds)

        