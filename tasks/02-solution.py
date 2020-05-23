""" Parameters

[a,b,c,d,a,b,c,d ...]

a = action
b, c = actor locations
d = result location index

opcodes: 1  +
         2  *
         99 halt

"""

import common
from copy import deepcopy


def run_program(opcodes, noun, verb):
    """ Runs through the opcodes. 

        >>> [99]
        [99]

        >>> run_program([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], 9, 10)
        [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
        
        (1 + 1 = 2)
        >>> run_program([1, 0, 0, 0, 99], 0, 0)
        [2, 0, 0, 0, 99]
        
        (3 * 2 = 6)
        >>> run_program([2, 3, 0, 3, 99], 3, 0)
        [2, 3, 0, 6, 99]

        (99 * 99 = 9801)
        >>> run_program([2, 4, 4, 5, 99, 0], 4, 4)
        [2, 4, 4, 5, 99, 9801]
        
        .
        >>> run_program([1, 1, 1, 4, 99, 5, 6, 0, 99], 1, 1)
        [30, 1, 1, 4, 2, 5, 6, 0, 99]

    """

    opcodes[1] = noun
    opcodes[2] = verb

    i = 0 
    while i < len(opcodes):
        op = opcodes[i]
        if op == 99:
            return opcodes

        val1 = opcodes[opcodes[i+1]]
        val2 = opcodes[opcodes[i+2]]
        r = opcodes[i+3]

        if op == 1:
            opcodes[r] = eval('val1 + val2')
        elif op == 2:
            opcodes[r] = eval('val1 * val2')
        else:
            return "err: ", i

        i += 4

    return opcodes


def find_noun_verb(opcodes):

    for i in range(100):
        for j in range(100):
            opcodes_copy = deepcopy(opcodes)
            output = run_program(opcodes_copy, i, j)[0]
            if output == 19690720:
                return (i, j)

    return (None, None)


#####
if __name__ == '__main__':
    import doctest
    doctest.testmod()  # verbose=True

    # Part 1
    opcodes = [int(item) for item in common.listify_input_string('02-input.txt')]
    print(run_program(opcodes, 12, 2)[0])

    # Part 2
    opcodes = [int(item) for item in common.listify_input_string('02-input.txt')]
    noun, verb = find_noun_verb(opcodes)
    print(100 * noun + verb)
