from client.client_ import Client
from client.login import Login
from client.main_menu import MainMenu
from client.room_view import RoomView
import socket


class Game:
    def __init__(self):
        self.login = None
        self.menu = None
        self.room_view = None
        self.client = None
        self.connect_to_server()

    def create_menu(self, room_names, artists):
        self.room_view = RoomView()
        self.menu = MainMenu(self.login.get_username(), room_names,
                             self.client, self.room_view, artists)
        self.menu.set_username('Username: ' + self.login.get_username())
        self.menu.show()
        self.room_view.menu = self.menu
        self.login.hide()
        self.menu.game_over.connect(self.quit_game)
        self.room_view.answer_selected.connect(self.client.send_answer)
        self.room_view.exit_requested.connect(self.client.exit_room)
        self.client.received_choices.connect(self.room_view.set_choices)
        self.client.received_start_message.connect(
            self.room_view.start_playing)
        self.client.received_room_scoreboard.connect(
            self.room_view.check_answer)
        self.room_view.ready.connect(self.client.send_ready_message)
        self.client.finished_writing.connect(self.room_view.set_filename)
        self.client.received_main_scoreboard.connect(
            self.menu.update_scoreboard)

    def quit_game(self):
        self.client.disconnect()
        self.login.show()
        self.connect_to_server()

    def connect_to_server(self):
        try:
            self.login = Login()
            self.client = Client()
            print('connect to server', self.client, self.client.sock)
            self.login.user_names_requested.connect(self.client.get_user_names)
            self.client.received_user_names.connect(
                self.login.validate_command)
            self.login.username_validated.connect(self.client.get_room_names)
            self.client.received_room_names.connect(self.create_menu)
            self.login.login_closed.connect(self.client.disconnect)
        except socket.error:
            print('Could not connect to server')
            exit()
