""" Day 7 """

from itertools import permutations
import common
from computer import Computer

TEST_PROG_1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
TEST_PHASES_1 = [4,3,2,1,0]

phase_perms = permutations(list(range(0, 5)))



##########
if __name__ == "__main__":
    program = TEST_PROG_1
    output = 0
    for phase in TEST_PHASES_1:
        print(phase, output)
        comp = Computer()
        output = comp.run_program(program=program, inputs=[phase, output])

    print("Thruster Signal:", output)

    # comp = Computer()

    # output = comp.run_program(program, inputs=[4,0])
    # print("Output:", output)
