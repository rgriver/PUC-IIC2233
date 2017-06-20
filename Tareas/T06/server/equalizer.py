from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import random
import os

"""
Basado en la ayudantía IO-Archivos del 2016-2
"""


class Equalizer:
    def __init__(self, genre):
        self.genre = genre
        self.paths = []
        self.f = random.uniform(0.3, 5)  # f
        self.n = random.randint(1, 10)  # n
        for filename in os.listdir('./songs/' + genre):
            self.paths.append('./songs/' + genre + '/' + filename)

    def choose_song(self, filename):
        # path = random.choice(self.paths)
        with open('./songs/' + self.genre + '/' + filename, 'rb') as f:
            return f.read()

    @staticmethod
    def convert_to_bytes(sample):
        if sample < 0:
            sample += 2 ** 16 - 1
        return sample.to_bytes(2, byteorder='little')

    def process_song(self, filename):
        song = self.choose_song(filename)
        header = song[:44]
        header = self.change_header(header)
        data = song[44:]
        channels = self.split_data(data)
        for i in range(self.n):
            channels[0] = self.filter(channels[0])
            channels[1] = self.filter(channels[1])

        data = bytearray()
        for i in range(len(channels[0])):
            data.extend(self.convert_to_bytes(channels[0][i]))
            data.extend(self.convert_to_bytes(channels[1][i]))

        return [header, data]

    @staticmethod
    def convert_to_int(data):
        size = len(data)
        return sum(data[i] << (i * 8) for i in range(size))

    def split_data(self, data):
        channels = {0: bytearray(), 1: bytearray()}
        channels_out = {0: list(), 1: list()}
        for i in range(0, len(data), 2):
            channels[int(i / 2) % 2].extend(data[i:i + 2])

        for channel in channels:
            for i in range(0, len(channels[channel]), 2):
                number = self.convert_to_int(channels[channel][i:i + 2])
                sample = (
                number - (2 ** 16 - 1)) if number >= 2 ** 15 else number
                channels_out[channel].append(sample)
        return channels_out

    @staticmethod
    def filter(data):
        new_data = list()
        for i in range(len(data)):
            if i == 0:
                new_data.append(data[0])
            else:
                value = int((new_data[i - 1] + data[i]) / 2)
                new_data.append(value)
        return new_data

    def change_header(self, header):
        new_header = list()
        fs = int(self.convert_to_int(header[24:28]) * self.f)

        bps = self.convert_to_int(header[34:36])
        nch = self.convert_to_int(header[22:24])
        br = int(fs * bps * nch / 8).to_bytes(4, byteorder='little')
        bo = int(bps * nch / 8).to_bytes(2, byteorder='little')

        new_header.append(fs.to_bytes(4, byteorder='little'))
        new_header.append(br)
        new_header.append(bo)
        return new_header
