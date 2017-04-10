import os


class GameLoader:
    def __init__(self):
        self.x = None

    def load_game(self):
        if os.path.isfile('game_data.txt'):
            return False
        return True


