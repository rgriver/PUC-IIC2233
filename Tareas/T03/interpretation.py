import errors
import core
from inspect import signature


def validate_command(command):
    name = command[0]
    if not isinstance(name, str):
        raise TypeError
    f = core.variables.get(name)
    if not(name in core.functions or f in core.functions.values()):
        raise errors.UndefinedFunction(name)
    return True


def execute(command):
    f = command[0]
    if len(command) == 1:
        raise errors.NoArguments
    if f is not core.functions['crear_funcion']:
        sig = signature(f)
        if len(command[1:]) != len(sig.parameters):
            raise errors.ArgumentError
    value = f(*command[1:])
    if value is not None:
        return value


def evaluate(expression):
    # print('Starting evaluation...')
    # print('I got this:', expression)

    expr = list(map(lambda x: replace(x), expression))

    if len(expr) > 0:
        if expr[0] in core.functions.values():
            if expr[0] is core.functions['asignar'] and len(expr) > 1:
                expr[1] = expression[1]
            return execute(expr)

    # print("It doesn't look like a function:", expression)
    return expr


def replace(element):
    if isinstance(element, str):
        if element in core.functions:
            return core.functions[element]
        elif element in core.variables:
            return core.variables[element]
    return element


def simplify(command):
    if len(command) > 0:
        if command[0] == 'do_if':
            if len(command[1:]) != 3:
                raise errors.ArgumentError
            value = simplify(command[2])
            if value is True:
                return simplify(command[1])
            elif value is False:
                return simplify(command[3])
            else:
                raise ValueError("'query_b' must return a boolean.\n")

    return evaluate(list(map(lambda x: simplify(x) if isinstance(x, list)
                             else x, command)))


def command_to_str(command):
    name = command[0]
    text = name + '('
    a = ''
    if len(command) > 1:
        arguments = list(command[1:])
        arguments = list(map(lambda x: simplify_argument(x), arguments))
        n = len(arguments)
        a = str(arguments).replace('"', '')
        a = a[1:-1]
    text += a
    text += ')'
    return text


def simplify_argument(argument):
    if isinstance(argument, list):
        if argument:
            if isinstance(argument[0], str):
                return "'" + argument[0] + "'*"
            else:
                argument = list(map(lambda x: simplify_argument(x), argument))
    return argument
