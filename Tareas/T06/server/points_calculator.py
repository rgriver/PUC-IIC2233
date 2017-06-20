class PointsCalculator:
    def __init__(self, room):
        self.users = room.users
        self.scoreboard = room.scoreboard

    def calculate(self, username, state, answer_time):
        points = state * (20 - answer_time)
        self.scoreboard[username] += points
        return points
