from math import *
from date_time import *

class Optimizer:
    def __init__(self, fires, resources, forecasts, user_date, fire_id):
        self.fires = fires
        self.resources = resources
        self.forecasts = forecasts
        self.date = DateTime()
        self.user_date = user_date
        self.step_size = 60  # in seconds
        self.fire_id = fire_id
        self.fire_lat = None
        self.fire_lon = None
        self.fire_r = 0
        self.fire_points = 0
        self.fire_power = None
        self.clouds_level = None

    def set_fire_data(self):
        line = self.fires.get_line(self.fire_id)
        self.fire_lat = line[1]
        self.fire_lon = line[2]
        self.fire_power = int(line[3])
        self.date.set_formatted_date_time(line[4])

    def get_current_points(self):
        self.set_fire_data()
        while self.date.get_formatted_date_time() <= \
                self.user_date.get_formatted_date_time():
            # self.fire_r += (500/3600) * self.step_size
            self.apply_weather_effect()
            self.fire_points = pi * pow(self.fire_r, 2) * self.fire_power
            self.date.add_seconds(self.step_size)
            if self.fire_points <= 0:
                break

    def set_step_size(self, seconds):
        self.step_size = seconds

    @staticmethod
    def calculate_distance(lat_1, lon_1, lat_2, lon_2):
        earth_radius = 6371008.8  # in meters
        lat_1 = radians(float(lat_1))
        lon_1 = radians(float(lon_1))
        lat_2 = radians(float(lat_2))
        lon_2 = radians(float(lon_2))
        delta_lat = lat_1 - lat_2
        delta_lon = lon_1 - lon_2
        a = sin(delta_lat / 2)**2 + cos(lat_1) * cos(lat_2) * \
            sin(delta_lon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        d = earth_radius * c
        return d

    def apply_weather_effect(self):
        self.fire_r += (500 / 3600) * self.step_size
        f = self.forecasts.get_data()
        start = '0'
        effect = 0
        idd = None
        self.clouds_level = None
        while True:
            line = next(f, None)
            if line is None:
                break
            line = line.strip()
            line = line.split(',')
            lat = float(line[5])
            lon = float(line[6])
            weather_r = float(line[7])
            end = line[2]
            date = self.date.get_formatted_date_time()
            d = self.calculate_distance(self.fire_lat, self.fire_lon, lat, lon)
            if self.fire_r + weather_r > d:
                if line[1] > start:
                    start = line[1]
                else:
                    continue
                if start <= date <= end:
                    idd = line[0]
                    effect = self.calculate_weather_effect(
                        line[3],
                        float(line[4]))

        self.fire_r += effect
        #print(str(self.date.get_formatted_date_time()) + ' ' + str(idd) + ' ' + str(effect) + ' ' + str(self.fire_points))

    def calculate_weather_effect(self, weather, value):
        effect = 0
        if weather == 'VIENTO':
            effect = self.calculate_wind_effect(value)
        elif weather == 'TEMPERATURA':
            effect = self.calculate_temperature_effect(value)
        elif weather == 'LLUVIA':
            effect = self.calculate_rain_effect(value)
        elif weather == 'NUBES':
            self.clouds_level = float(value)
        return effect

    def calculate_wind_effect(self, value):
        effect = (float(value) / 100) * self.step_size
        return effect

    def calculate_temperature_effect(self, value):
        value = float(value)
        if value <= 30:
            return 0
        else:
            effect = (value - 30) * (25/3600) * self.step_size
            return effect

    def calculate_rain_effect(self, value):
        effect = value * (50/3600) * self.step_size * -1
        return effect

    def find_min_points(self):
        pass








