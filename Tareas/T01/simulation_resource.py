from date_time import *

class SimulationResource:
    def __init__(self, info, step, distance):
        self.id = info[0]
        self.type = info[1]
        self.speed = float(info[4])
        self.max_work_time = int(info[5]) * 3600
        self.delay = int(info[6]) * 3600
        self.points = int(info[7]) / 3600
        self.cost = int(info[8])
        self.distance = float(distance)
        self.dist_to_headquarters = 0
        self.dist_to_fire = float(distance)
        self.effect = 0
        self.step = step
        self.sleep_time = 0
        self.work_time = 0
        self.state = 'IDLE'
        self.dates_list = []
        self.date = DateTime()
        self.word = ''

    def set_date(self, date):
        self.date.set_formatted_date_time(date)

    def get_id(self):
        return self.id

    def move_to_fire(self, request):
        dist = self.speed * self.step
        if not request:
            self.state = 'TO_HEADQUARTERS'
        elif self.dist_to_fire - dist < 0:
            self.dist_to_headquarters = self.distance
            self.dist_to_fire = 0
            self.add_date_to_word()
            self.state = 'WORK'
        else:
            self.dist_to_fire -= dist
            self.dist_to_headquarters += dist

    def move_to_headquarters(self):
        dist = self.speed * self.step
        if self.dist_to_headquarters - dist < 0:
            self.dist_to_fire = self.distance
            self.dist_to_headquarters = 0
            self.add_date_to_word()
            self.state = 'SLEEP'
        else:
            self.dist_to_headquarters -= dist
            self.dist_to_fire += dist

    def work(self, request):
        effect = 0
        if self.work_time + self.step >= self.max_work_time or not request:
            self.work_time = 0
            self.add_date_to_word()
            self.state = 'TO_HEADQUARTERS'
        else:
            effect = self.points * self.step
            self.effect += effect
            self.work_time += self.step
        return effect

    def handle_request(self, request):
        if request:
            self.create_new_word()
            self.state = 'TO_FIRE'
        else:
            self.state = 'IDLE'

    def sleep(self, request):
        if self.sleep_time + self.step >= self.delay:
            self.sleep_time = 0
            self.add_date_to_word()
            if self.effect:
                self.word += ',' + str(self.effect)
                self.append_word()
                self.effect = 0
            self.handle_request(request)
        else:
            self.sleep_time += self.step

    def update(self, request):
        effect = 0
        if self.state == 'IDLE':
            self.handle_request(request)
        elif self.state == 'TO_FIRE':
            self.move_to_fire(request)
        elif self.state == 'WORK':
            effect = self.work(request)
        elif self.state == 'TO_HEADQUARTERS':
            self.move_to_headquarters()
        elif self.state == 'SLEEP':
            self.sleep(request)

        self.date.add_seconds(self.step)
        return effect

    def add_date_to_word(self):
        self.word += ',' + self.date.get_formatted_date_time()

    def append_word(self):
        self.dates_list.append(self.word)

    def get_dates_list(self):
        return self.dates_list

    def create_new_word(self):
        self.word = ''
        self.word += '\n' + str(self.id) + ',' + \
                     self.date.get_formatted_date_time()

