from optimizer import *
from math import *
from simulation_resource import *
import os

class TimeOptimizer(Optimizer):
    def __init__(self, fires, resources, forecasts, user_date, fire_id):
        super(TimeOptimizer, self).__init__(fires, resources, forecasts,
                                            user_date, fire_id)
        self.times = []

    def optimize(self):
        if not os.path.exists('Reportes Estrategias de Extinción'):
            os.makedirs('Reportes Estrategias de Extinción')
        file_name = self.fire_id + '_time.txt'
        path = os.path.join('Reportes Estrategias de Extinción', file_name)
        report_file = open(path, 'w+')
        report_file.write(self.fire_id)
        self.get_current_points()
        sim_resources = []
        f = self.resources.get_data()
        while True:
            line = next(f, None)
            if line is None:
                break
            line = line.strip()
            line = line.split(',')
            distance = self.calculate_distance(line[2],
                                               line[3],
                                               self.fire_lat,
                                               self.fire_lon)
            resource = SimulationResource(line, self.step_size, distance)
            resource.set_date(self.date.get_formatted_date_time())
            sim_resources.append(resource)

        while True:
            self.apply_weather_effect()
            for r in sim_resources:
                r.set_date(self.date.get_formatted_date_time())
                self.fire_points -= r.update(1)
                if self.fire_points <= 0:
                    break
            if self.fire_points <= 0:
                break
            self.fire_r = sqrt(self.fire_points / (pi * self.fire_power))
            self.date.add_seconds(self.step_size)

        while True:
            all_checked = True
            for r in sim_resources:
                r.set_date(self.date.get_formatted_date_time())
                r.update(0)
                all_checked = all_checked and (r.state == 'IDLE')
            if all_checked:
                break
            self.date.add_seconds(self.step_size)

        for r in sim_resources:
            dates_list = r.get_dates_list()
            if dates_list:
                for d in dates_list:
                    report_file.write(d)
        report_file.close()







