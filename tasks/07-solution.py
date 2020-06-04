""" Day 7 """

from itertools import permutations
import common
from computer import Computer

TEST_PHASES_1 = [4,3,2,1,0]
TEST_PROG_1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]

TEST_PHASES_2 = [9,7,8,5,6]
TEST_PROG_2 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

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
        # print(phase, output)
        comp = Computer()
        output = comp.run_program(program=TEST_PROG_1, inputs=[phase, output])

    print("\nTest 1 Thruster Signal:", output)

    # output = 0
    # # import pdb; pdb.set_trace()
    # while True:
    #     for phase in TEST_PHASES_2:
    #         # print(phase, output)
    #         comp = Computer()
    #         output = comp.run_program(program=TEST_PROG_2, inputs=[phase, output])

    # print("\nTest 2 Thruster Signal:", output)

    program = [int(item) for item in common.listify_input_string('07-input.txt')]

    # Part 1
    print("\nPart 1:", do_part1(program))  # answer 65464

    # Part 2
    """ I still don't understand how it's meant to work. I need to study the
        solution I used still, but it was the first one that I could plug in my
        puzzle input relatively easily.

        answer 1518124
    """