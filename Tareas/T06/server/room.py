import threading
import random
from server.points_calculator import PointsCalculator
from server.equalizer import Equalizer
from PyQt5.QtCore import QTimer
import pickle
import os
import time


class Room:
    def __init__(self, name):
        self.name = name
        self.current_song = None
        self.songs = []
        self.users = dict()
        self.answers = None
        self.correct_answer = None
        self.time = 0
        self.equalizer = Equalizer(name)
        self.titles = dict()
        self.artists = dict()
        self.set_songs_info()
        self.scoreboard = dict()
        self.time_table = list()
        self.active = False
        self.correct_num = None
        self.use_equalizer = False
        self.path = './songs/' + self.name + '/'
        self.users_state = dict()

    def set_songs_info(self):
        for filename in os.listdir('./songs/' + self.name):
            [artist, title] = filename[:-4].split('-')
            self.artists[artist.strip()] = filename
            self.titles[title.strip()] = filename

    def play(self):
        print(self.time)
        if self.users:
            if self.time < 20:
                self.time += 1
                timer = threading.Timer(1, self.play)
                timer.start()
            elif self.time == 20:
                self.time = 0
                # self.choose_song()
        else:
            self.time = 0

    def set_time(self):
        for user in self.users:
            user.send(str(self.time).encode('utf8'))

    def accept_user(self, client_sock, username):
        print('new user in', self.name, ' room')
        self.users[client_sock] = username
        self.scoreboard[username] = 0
        self.users_state[client_sock] = False
        if len(self.users) == 1:
            print('first')
            self.choose_song()

    def remove_user(self, sock):
        username = self.users[sock]
        del self.users[sock]
        del self.scoreboard[username]
        del self.users_state[sock]
        print('user ', username, 'removed from ', self.name, ' room')

    def choose_song(self):
        self.time_table = list()
        choices_dict = random.choice([self.artists, self.titles])
        choices_list = list(choices_dict)
        correct_answer = random.choice(choices_list)
        choices_list.remove(correct_answer)
        filename = choices_dict[correct_answer]
        print(filename, correct_answer)
        self.correct_num = random.randint(1, 4)
        choices_command = ['send_choices']
        for i in range(4):
            if i + 1 == self.correct_num:
                choices_command.append(correct_answer)
            else:
                choice = random.choice(choices_list)
                choices_command.append(choice)
                choices_list.remove(choice)
        choices_command = pickle.dumps(choices_command)
        time.sleep(1)
        for user in self.users:
            user.send(choices_command)
        time.sleep(1)
        for user in self.users:
            user.send(pickle.dumps(['send_song', filename]))
            with open(self.path + filename, 'rb') as f:
                length = os.path.getsize(self.path + filename)
                print(length)
                user.send(self.convert_to_bytes(length))
                d = f.read(65536)
                while d:
                    user.send(d)
                    time.sleep(0.001)
                    d = f.read(65536)
        time.sleep(2)
        start_command = pickle.dumps(['start'])
        for user in self.users:
            user.send(start_command)
        self.play()

    def check_answer(self, sock, answer, answer_time):
        username = self.users[sock]
        state = answer is self.correct_num
        points = state * (20 - answer_time)
        self.scoreboard[username] += points
        if state:
            label = 'OK'
        else:
            label = 'WRONG'
        self.time_table.append((username, answer_time,
                                self.scoreboard[username], label))
        command = pickle.dumps(['update_room_scoreboard', state,
                                self.time_table])
        sock.send(command)
        return points

    '''
    https://stackoverflow.com/questions/20007319/how-to-do-a-large-text-file
    -transfer-in-python
    '''
    def process_song(self, filename):
        if self.use_equalizer:
            header, data = self.equalizer.process_song(filename)
        else:
            with open('./songs/' + self.name + '/' + filename, 'rb') as f:
                song = f.read(2048)
            header = song[:44]
            data = song[44:]
        return header, data

    @staticmethod
    def convert_to_bytes(value):
        data = bytearray()
        data.append(value & 255)
        for i in range(3):
            value >>= 8
            data.append(value & 255)
        return data

    def check_users(self, sock):
        self.users_state[sock] = True
        if all(self.users_state.values()):
            for s in self.users_state:
                self.users_state[s] = False
        self.choose_song()


