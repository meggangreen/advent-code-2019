""" Day 7 """

import common
from computer import Computer

TEST_IN = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]



##########
if __name__ == "__main__":
    program = TEST_IN
    comp = Computer()

    comp.run_program(program)
