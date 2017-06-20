import socket
import threading
import json
import pickle
import os
from server.room import Room


class Server:
    HOST = '192.168.0.11'
    PORT = 3490

    def __init__(self):
        self.scores = dict()
        self.users = dict()
        self.users_by_sock = dict()
        self.user = None
        self.host = Server.HOST
        self.port = Server.PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(2)
        self.connections = []
        self.rooms = []
        self.generate_rooms()
        self.connect_client()
        self.thread = threading.Thread(target=self.connect_client, daemon=True)
        self.thread.start()
        self.rooms_controller = None

    def connect_client(self):
        while True:
            print('trying to connect')
            client_sock, address = self.sock.accept()
            print('New connection!')
            client_thread = threading.Thread(target=self.receive_messages,
                                             args=(client_sock, ))
            client_thread.start()
            self.connections.append((client_sock, client_thread))
            self.scores[client_sock] = 0

    def receive_messages(self, client_sock):
        while True:
            data = client_sock.recv(2048)
            if not data:
                break
            data = pickle.loads(data)
            print(data[0])
            if data[0] == 'quit_game':
                self.disconnect_client(client_sock)
                break
            elif data[0] == 'get_room_names':
                command = pickle.dumps(['send_room_names',
                                        [r.name for r in self.rooms],
                                        [list(r.artists.keys())[:2] for r in
                                         self.rooms]])
                client_sock.send(command)
            elif data[0] == 'get_user_names':
                command = pickle.dumps(['send_user_names',
                                        list(self.users.values())])
                client_sock.send(command)
            elif data[0] == 'send_username':
                self.users[data[1]] = client_sock
                self.users_by_sock[client_sock] = data[1]
            elif data[0] == 'enter_room':
                self.rooms_controller.enter_room(user_sock=client_sock,
                                                 username=data[1],
                                                 room_name=data[2])
            else:
                # room_controller = RoomController(self.rooms)
                self.rooms_controller.process_data(data, client_sock)

    def generate_rooms(self):
        for directory in os.listdir('./songs'):
            if not directory.startswith('.'):
                self.rooms.append(Room(directory))
        self.rooms_controller = RoomController(self.rooms, self.scores,
                                               self.connections,
                                               self.users_by_sock)

    def disconnect_client(self, client_sock):
        for connection in self.connections:
            if connection[0] is client_sock:
                self.connections.remove(connection)
                del self.scores[client_sock]
                if client_sock in self.users_by_sock:
                    del self.users_by_sock[client_sock]
                break


class RoomController:
    def __init__(self, rooms, scores, connections, users_by_sock):
        self.rooms = dict()
        self.assigned_rooms = dict()
        self.scores = scores
        self.connections = connections
        self.users_by_sock = users_by_sock
        for room in rooms:
            self.rooms[room.name] = room

    def process_data(self, data, client_sock):
        command = {
            'send_answer': self.check_answer,
            'exit_room': self.exit_room,
            'ready': self.check_users
        }[data[0]]
        if len(data) > 0:
            command(client_sock, *data[1:])
        else:
            command()

    def enter_room(self, room_name, user_sock, username):
        room = self.rooms[room_name]
        self.users_by_sock[user_sock] = username
        self.assigned_rooms[user_sock] = room
        room.accept_user(user_sock, username)

    def check_answer(self, sock, answer, answer_time):
        room = self.assigned_rooms[sock]
        points = room.check_answer(sock, answer, answer_time)
        self.scores[sock] += points
        for sock, thread in self.connections:
            print(self.users_by_sock)
            s = [(self.users_by_sock[x[0]], x[1]) for x in self.scores.items()]
            s.sort(key=lambda x: x[1], reverse=True)
            sock.send(pickle.dumps(['update_main_scoreboard', s]))

    def exit_room(self, sock):
        print('exit')
        room = self.assigned_rooms[sock]
        del self.assigned_rooms[sock]
        room.remove_user(sock)

    def check_users(self, sock):
        room = self.assigned_rooms[sock]
        room.check_users(sock)

if __name__ == '__main__':
    server = Server()
