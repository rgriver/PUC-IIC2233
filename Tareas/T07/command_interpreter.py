import re


class CommandInterpreter:
    def __init__(self):
        self.get_pattern = re.compile(r'^(/get)\s+([0-9]+)$')
        self.post_pattern = re.compile(r'^(/post)\s+([0-9]+)\s+[*](.+)$')
        self.label_pattern = \
            re.compile(r'^(/label)\s+([0-9]+)\s+([a-zA-Z0-9\s]+)$')
        self.close_pattern = re.compile(r'^(/close)\s+([0-9]+)$')

    def process_text(self, raw_text):
        text = raw_text.strip()
        groups = ('Error', "Sorry, I didn't get that.")
        if self.get_pattern.match(text):
            groups = self.get_pattern.match(text).groups()
        elif self.post_pattern.match(text):
            groups = self.post_pattern.match(text).groups()
        elif self.label_pattern.match(text):
            groups = self.label_pattern.match(text).groups()
        elif self.close_pattern.match(text):
            groups = self.close_pattern.match(text).groups()
        return groups
