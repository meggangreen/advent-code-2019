""" A collection of common functions used in puzzle solutions. """

def listify_input_file(puzzle_input):
    """ Returns a list of input from a multi-line file. """

    with open(puzzle_input) as file:
        return file.readlines()


def listify_input_string(puzzle_input):
    """ Returns a list of input from a comma-delimited string in file. """

    with open(puzzle_input) as file:
        return file.read().split(',')

