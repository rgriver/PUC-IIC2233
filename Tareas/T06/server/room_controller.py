import pickle


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
