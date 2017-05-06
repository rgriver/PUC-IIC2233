import data_reading

command = ''

message = ''


def placeholder(whatever):
    pass

show = placeholder


class RqlError(Exception):
    def __init__(self, msg):
        out = "Error de consulta: " + command + '\nCausa: ' + msg
        show(out)
        data_reading.output.append(out)


class ArgumentError(RqlError):
    def __init__(self, msg="Wrong number of arguments.\n"):
        super(ArgumentError, self).__init__(msg)


class InvalidReference(RqlError):
    pass


class MathError(RqlError):
    def __init__(self, msg):
        super(MathError, self).__init__(msg)


class ImpossibleProcessing(RqlError):
    def __init__(self, msg):
        super(ImpossibleProcessing, self).__init__(msg)
        # show("Impossible to process argument(s)")


class UndefinedFunction(RqlError):
    def __init__(self, name):
        super(UndefinedFunction, self).__init__("Undefined function '" + name + "'.\n")
        # show("Undefined function '" + name + "'.\n")


class NoArguments(RqlError):
    def __init__(self):
        super(NoArguments, self).__init__('No arguments provided.\n')
        # show('No arguments provided.\n')


class ReservedName(RqlError):
    def __init__(self, name):
        super(ReservedName, self).__init__("Forbidden use of built-in "
                                           "name '" + name + "'.\n")

