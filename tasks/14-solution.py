""" Day 14

    Notes:
    - "FUEL" is the goal -- root
    - products from "ORE" are the starting point -- leaves
    - 1xFUEL = sum(leaves) ORE requirements

"""

TEST_INPUT_1 = {('A', 10):   [('ORE', 10)],
                ('B', 1):    [('ORE', 1)],
                ('C', 1):    [('A': 7), ('B', 1)],
                ('D', 1):    [('A', 7), ('C', 1)],
                ('E', 1):    [('A', 7), ('D', 1)],
                ('FUEL', 1): [('A', 7), ('E', 1)],
               }


