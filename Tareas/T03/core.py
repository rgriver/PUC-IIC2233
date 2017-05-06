
data_types = (
    'int',
    'str',
    'None',
    'Funcion',
    'Columna',
    'Consulta',
    'any',
)

comparison_operators = {
    '>': lambda x, y: x > y,
    '>=': lambda x, y: x >= y,
    '<': lambda x, y: x < y,
    '<=': lambda x, y: x <= y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y
}

arithmetic_operators = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
}


def placeholder(whatever):
    pass

show = placeholder

variables = {}
functions = {}
user_functions = []
