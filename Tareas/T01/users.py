import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Users:
    def __init__(self, file_name):
        self.file_name = file_name

    def check_credentials(self, name, password):
        file = open(self.file_name, 'r')
        for line in file:
            line = line.split(',')
            if name == str(line[1]):
                if password == str(line[2]):
                    return True
                else:
                    return False
        return False

    def add_user(self, name, password, resource_id):
        file = open(self.file_name, 'r+')
        line = None
        for line in file:
            if line.split(',')[1] == name:
                return False
        line = line.split(',')
        last_id = int(line[0])
        new_id = last_id + 1
        file.write('\n' + str(new_id) + ',' + name + ',' + password + ',' + resource_id)
        return True

    def get_user(self, id):
        file = open(self.file_name, 'r')
        name = password = resource_id = ''
        for line in file:
            line = line.split(',')
            if line[0] == id:
                name = line[1]
                password = line[2]
                resource_id = line[3]
        return name, password, resource_id

    def get_resource_id(self, name):
        file = open(self.file_name, 'r')
        resource_id = ''
        for line in file:
            line = line.strip()
            line = line.split(',')
            if line[1] == name:
                resource_id = line[3]
                break
        return resource_id
