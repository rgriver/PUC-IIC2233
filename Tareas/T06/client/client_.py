from PyQt5.QtCore import QObject, pyqtSignal
import pickle
import threading
import socket
import os


class Client(QObject):
    HOST = '192.168.0.11'
    PORT = 3490

    menu_creation_requested = pyqtSignal(list)
    received_user_names = pyqtSignal(list)
    received_room_names = pyqtSignal(list, list)
    room_creation_requested = pyqtSignal(str)
    received_choices = pyqtSignal(str, str, str, str)
    received_start_message = pyqtSignal()
    received_room_scoreboard = pyqtSignal(bool, list)
    finished_writing = pyqtSignal(str)
    received_main_scoreboard = pyqtSignal(list)

    def __init__(self):
        super(Client, self).__init__()
        self.alive = True
        self.host = Client.HOST
        self.port = Client.PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.receiver = threading.Thread(target=self.receive_message)
        self.receiver.daemon = True
        self.receiver.start()
        self.filename = None

    def receive_message(self):
        while self.alive:
            try:
                data = self.sock.recv(2048)
            except OSError:
                break
            if not data:
                break
            data = pickle.loads(data)
            command = {
                'send_room_names': self.create_room_buttons,
                'send_user_names': self.send_user_names,
                'send_choices': self.set_choices,
                'send_song': self.receive_song,
                'start': self.send_start_signal,
                'update_room_scoreboard': self.update_room_scoreboard,
                'update_main_scoreboard': self.update_main_scoreboard
            }[data[0]]

            if len(data) > 0:
                command(*data[1:])
            else:
                command()

    def create_main_menu(self, room_names):
        self.menu_creation_requested.emit([room_names, self])

    def send_user_names(self, user_names):
        self.received_user_names.emit(user_names)

    def enter_room(self, username, room_name):
        command = ['enter_room', username, room_name]
        command = pickle.dumps(command)
        self.sock.send(command)

    def disconnect(self):
        self.sock.send(pickle.dumps(['quit_game']))
        self.alive = False
        self.sock.close()

    def create_room(self, room_name):
        self.room_creation_requested.emit(room_name)

    def create_room_buttons(self, room_names, artists):
        self.received_room_names.emit(room_names, artists)

    def get_room_names(self):
        self.sock.send(pickle.dumps(['get_room_names']))

    def get_user_names(self):
        self.sock.send(pickle.dumps(['get_user_names']))

    def send_answer(self, answer, answer_time):
        self.sock.send(pickle.dumps(['send_answer', answer, answer_time]))

    def exit_room(self):
        self.sock.send(pickle.dumps(['exit_room']))

    def set_choices(self, a, b, c, d):
        self.received_choices.emit(a, b, c, d)

    def receive_song(self, filename):
        if self.filename is not None:
            if os.path.isfile(self.filename):
                os.remove(self.filename)
        self.filename = filename
        size = self.sock.recv(4)
        size = self.convert_to_int(size)
        print(size)
        current_size = 0
        buffer = b''
        while current_size < size:
            data = self.sock.recv(65536)
            if not data:
                break
            if len(data) + current_size > size:
                data = data[:size - current_size]
            buffer += data
            current_size += len(data)
        with open(filename, 'wb') as fw:
            fw.write(buffer)
        self.finished_writing.emit(filename)

    @staticmethod
    def convert_to_int(value):
        data = 0
        for i in range(4):
            data += value[i] << (i * 8)
        return data

    def send_start_signal(self):
        self.received_start_message.emit()

    def update_room_scoreboard(self, state, table):
        self.received_room_scoreboard.emit(state, table)

    def send_ready_message(self):
        self.sock.send(pickle.dumps(['ready']))

    def update_main_scoreboard(self, table):
        self.received_main_scoreboard.emit(table)
