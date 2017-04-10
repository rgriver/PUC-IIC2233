import csv


class Database:
    def __init__(self, filename):
        self.filename = filename
        self.current_line = None

    def get_data(self, d=','):
        f = open(self.filename)
        file = csv.reader(f, delimiter=d)
        return file

    def get_lines(self, d=','):
        with open(self.filename) as f:
            file = csv.reader(f, delimiter=d)
            l = LinkedList(*file)
        return l