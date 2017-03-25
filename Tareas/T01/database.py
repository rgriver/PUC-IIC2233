class Database:
    def __init__(self, filename):
        self.filename = filename

    def add_line(self, new_line):
        file = open(self.filename, 'r+')
        for line in file:
            pass
        line = line.split(',')
        last_id = int(line[0])
        new_id = str(last_id + 1)
        file.write('\n' + str(new_id) + ',' + new_line)

    def get_line(self, line_id):
        file = open(self.filename, 'r')
        for line in file:
            line = line.strip('\n')
            line = line.split(',')
            if line[0] == line_id:
                return line
        return []

    def get_data(self):
        f = open(self.filename, 'r')
        next(f)
        return f

