import csv
from linked_list import *


class BordersDatabase:
    def __init__(self):
        self.filename = 'borders.csv'
        self.current_line = None

    def get_data(self):
        f = open(self.filename)
        file = csv.reader(f, delimiter=';')
        return file

    def get_lines(self):
        with open(self.filename) as f:
            file = csv.reader(f, delimiter=';')
            l = LinkedList(*file)
        return l
