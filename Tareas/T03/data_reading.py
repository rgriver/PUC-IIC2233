import errors

output = []


def get_data(filename):
    with open(filename) as f:  # raise FileNotFoundError if file does not exist
        for line in f:
            yield line.strip().split(";")


def get_column(filename, column):
    data = get_data(filename)
    first_line = next(data)
    first_line = list(map(lambda x: column in x, first_line))
    if not any(first_line):
        raise errors.ImpossibleProcessing("'" + column + "' is not a "
                                                         "column.\n")
    index = first_line.index(True)  # raise ValueError if not in list
    try:
        return [float(x[index]) for x in data]
    except ValueError:
        return [x[index] for x in data]


def get_str(x):
    num = str(x[0] + 1)
    text = '-------- CONSULTA ' + num + '--------\n' + str(x[1])
    return text


def write_data():
    global output
    if output:
        f = open('resultados.txt', 'w+')
        f.writelines(list(map(lambda x: get_str(x), enumerate(output))))
        f.close()
        output = []
