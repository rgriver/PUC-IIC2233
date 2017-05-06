import errors
import core
import data_reading
import interpretation
import numpy as np
import os
from math import pi, e, ceil, floor
from matplotlib import pyplot as plt
from functools import reduce


def assign(variable, parameter):

    if not isinstance(variable, str):
        raise TypeError("'variable' must be of type 'str'.\n")
    if variable in core.functions:
        raise errors.ReservedName(variable)

    core.variables[variable] = parameter
    if isinstance(parameter, str):
        if parameter in core.functions:
            core.variables[variable] = core.functions[parameter]
    # print(core.variables.keys())


def create_function(model, *parameters):
    if not isinstance(model, str):
        raise TypeError("'model' must be type string\n")
    if model == 'normal':
        if len(parameters) != 2:
            raise errors.ArgumentError("Normal distribution expects "
                                       "2 parameters.\n")
        mu = parameters[0]
        sigma = parameters[1]
        if sigma <= 0:
            raise ValueError("'sigma' must be a positive number.\n")

        def normal(x):
            y = (1 / ((2 * pi * (sigma ** 2)) ** 0.5))\
                * e ** (-0.5 * (((x - mu) / sigma) ** 2))
            return y
        return normal
    elif model == 'exponencial':
        if len(parameters) != 1:
            raise errors.ArgumentError("Exponential distribution expects "
                                       "1 parameter.\n")
        nu = parameters
        if nu < 0:
            raise ValueError("'nu' must be a positive number.\n")

        def exponential(x):
            y = nu * (e ** (- nu * x))
            return y
        return exponential
    elif model == 'gamma':
        if len(parameters) != 2:
            raise errors.ArgumentError("Gamma distribution expects "
                                       "2 parameters.\n")
        nu = parameters[0]
        k = parameters[0]

        fac = reduce(lambda x, y: x * y, range(1, k)) # 1...k - 1

        def gamma(x):
            if x < 0:
                raise ValueError("'x' must be non-negative.\n")
            y = ((nu ** k) / fac) * (x ** (k - 1)) * (e ** (-nu * x))
            return y
        return gamma
    else:
        raise ValueError("'model' must be a valid probability distribution.\n")


def plot(column, option):
    if not check_numeric_iter(column):
        raise TypeError("Expected a column of numbers.\n")
    if isinstance(option, str):
        if option == 'numerico':
            var_x = range(len(list(column)))
        elif option == 'normalizado':
            s = sum(column)
            var_x = list(map(lambda x: x / s, range(len(list(column)))))
        elif 'rango:' in option:
            r = option.replace('rango:', '')
            r = r.split(',')
            if len(r) != 3:
                raise ValueError("'Option' must specify a valid range\n")
            try:
                map(lambda x: float(x), r)
            except:
                raise ValueError("Range must be set by a group of numbers.\n")
            r = list(map(lambda x: float(x), r))
            if r[0] > r[2] and r[1] > 0:
                raise ValueError("'Step' must be less than zero\n")
            elif r[0] < r[2] and r[1] < 0:
                raise ValueError("'Step' must be greater than zero\n")
            var_x = list(generate_range(*r))
        else:
            raise TypeError("'" + option + "' is an invalid option\n")
    elif check_numeric_iter(option):
        var_x = option
    else:
        raise TypeError("'option' must be a string or column\n")

    if len(list(var_x)) != len(list(column)):
        raise ValueError("'column' and 'option' must have the same size\n")
    plt.xscale('linear')
    plt.plot(np.array(list(var_x)), column, 'r')
    plt.show()


def extract_column(filename, column):
    if not isinstance(filename, str):
        raise TypeError("'filename' must be a string\n")
    if not isinstance(column, str):
        raise TypeError("'column' must be a string")
    if not os.path.exists(filename + '.csv'):
        raise errors.ImpossibleProcessing("'" + filename + "' does "
                                          "not exist.\n")
    return data_reading.get_column(filename + '.csv', column)


def filter_column(column, symbol, value):
    if not isinstance(column, list):
        raise TypeError("Expected a list\n")
    if not isinstance(symbol, str):
        raise TypeError("Symbol must be a string\n")
    elif symbol not in core.comparison_operators:
        raise TypeError("Symbol must be a comparison operator\n")
    if not isinstance(value, (int, float)):
        raise TypeError("Value must be a number\n")
    return [x for x in column if
            core.comparison_operators[symbol](x, value)]


def perform_operation(column, symbol, value):
    if not check_numeric_iter(column):
        raise TypeError('Expected a column of numbers\n')
    if not isinstance(symbol, str):
        raise TypeError("'symbol' must be a string\n")
    if not isinstance(value, (int, float)):
        raise TypeError("'value' must be a number\n")
    if symbol in core.arithmetic_operators:
        f = core.arithmetic_operators[symbol]
        c = map(lambda x: f(x, value), column)
    elif symbol == '>=<':
        if value <= 0:
            raise ValueError("'value' must be non-negative.")
        c = map(lambda x: round(x, value), column)
    else:
        raise ValueError("'symbol' must be a valid operator.\n")
    return list(c)


def evaluate(function, start, end, increment):
    if not hasattr(function, '__call__'):
        raise TypeError("Expected object of type 'function'")
    if not isinstance(start, (int, float)):
        raise TypeError("'start' must be a number.\n")
    if not isinstance(end, (int, float)):
        raise TypeError("'end' must be a number.\n")
    if not isinstance(increment, (int, float)):
        raise TypeError("'increment' must be a number.\n")
    if start > end:
        raise ValueError("'start' must be less than 'end'.\n")
    column = generate_range(start, increment, end)
    return list(map(lambda x: function(x), column))


def compare_column(column_a, symbol, command, column_b):
    if not check_numeric_iter(column_a):
        raise TypeError("'column_1' must be a column of numbers.\n")
    if not check_numeric_iter(column_b):
        raise TypeError("'column_2' must be a column of numbers.\n")
    if not isinstance(symbol, str):
        raise ValueError("'symbol' must be of type 'str'")
    if symbol not in core.comparison_operators:
        raise ValueError("'symbol' must be a comparison operator.\n")
    commands = ['LEN', 'PROM', 'DESV', 'MEDIAN', 'VAR']
    if command not in map(lambda x: core.functions[x], commands):
        raise ValueError("'command' is not a valid function.\n")
    f = command
    comp = core.comparison_operators[symbol]
    a = f(column_a)
    b = f(column_b)
    comparison = comp(a, b)
    return comparison


def compare(num_a, symbol, num_b):
    if not isinstance(num_a, (int, float)):
        raise TypeError('Number_1 must be number\n')
    if not isinstance(num_b, (int, float)):
        raise TypeError('Number_2 must be a number\n')
    if symbol not in core.comparison_operators:
        raise TypeError('Symbol must be comparison operator\n')
    return core.comparison_operators[symbol](num_a, num_b)


def mean(data):
    if not check_numeric_iter(data):
        raise TypeError("'data' must be of type 'column'.'")
    return sum(data) / len(data)


def length(data):
    if not check_numeric_iter(data):
        raise TypeError("'data' must be of type 'column'.'")
    return len(data)


def std(data):
    if not check_numeric_iter(data):
        raise TypeError("'data' must be of type 'column'.'")
    n = len(data)
    mu = sum(data) / n
    if n == 1:
        raise errors.MathError("Division by zero.\n")
    sigma = (sum(map(lambda x: (x - mu) ** 2, data)) / (n - 1)) ** 0.5
    return sigma


def median(data):
    if not check_numeric_iter(data):
        raise TypeError("'data' must be of type 'column'.'")
    data = list(data)
    mid = int(len(data) / 2)
    if len(data) % 2 == 0:
        x = (data[mid] + data[mid - 1]) / 2
    else:
        x = data[mid]
    return x


def var(data):
    sigma_sq = std(data) ** 2
    return sigma_sq


def check_numeric_iter(data):
    try:
        iter(data)
        valid_data = True
    except TypeError:
        valid_data = False
    # valid_data &= isinstance(data, (list, set, tuple))
    if valid_data:
        valid_data &= len(list(data)) > 0
        valid_data &= all(map(lambda x: isinstance(x, (int, float)), data))
    if not valid_data:
        return False
    return True


# Special function
def do_if(query_a, query_b, query_c):
    pass  # Check interpretation module


def generate_range(a, step, b):
    i = a
    while min(a, b) <= i <= max(a, b):
        yield i
        i += step


core.functions['asignar'] = assign
core.functions['crear_funcion'] = create_function
core.functions['graficar'] = plot
core.functions['extraer_columna'] = extract_column
core.functions['filtrar'] = filter_column
core.functions['operar'] = perform_operation
core.functions['evaluar'] = evaluate
core.functions['LEN'] = length
core.functions['PROM'] = mean
core.functions['DESV'] = std
core.functions['MEDIAN'] = median
core.functions['VAR'] = var
core.functions['comparar_columna'] = compare_column
core.functions['comparar'] = compare
core.functions['do_if'] = do_if
