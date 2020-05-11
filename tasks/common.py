""" A collection of common functions used in puzzle solutions. """

def listify_input_file(puzzle_input):
    """ Returns a list of input contained in the day's input.txt file. """

    with open(puzzle_input) as file:
        return file.readlines()



