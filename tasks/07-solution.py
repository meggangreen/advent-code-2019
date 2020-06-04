""" Day 7 """

from itertools import permutations
import common
from computer import Computer

TEST_PROG_1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
TEST_PHASES_1 = [4,3,2,1,0]

def do_part1(program):
    phase_perms = permutations(list(range(0, 5)))

    max_out = 0
    for perm in phase_perms:
        thruster_out = run_amplifiers(program, perm)
        max_out = max(max_out, thruster_out)
    
    return max_out


def run_amplifiers(program, perm):
    output = 0
    for phase in perm:
        # print(phase, output)
        comp = Computer()
        output = comp.run_program(program=program, inputs=[phase, output])
    
    return output


##########
if __name__ == "__main__":
    output = 0
    for phase in TEST_PHASES_1:
        print(phase, output)
        comp = Computer()
        output = comp.run_program(program=TEST_PROG_1, inputs=[phase, output])

    print("Test Thruster Signal:", output)

    program = [int(item) for item in common.listify_input_string('07-input.txt')]

    # Part 1
    print("Part 1:", do_part1(program))
