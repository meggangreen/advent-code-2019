""" Day 9

    - add relative mode - 2
    - add rel_base
    - add opcode 9 - jump rel_base

"""
import common
from computer import Computer

TEST_PROG_1 = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]

##########
if __name__ == "__main__":
    program = [int(n) for n in common.listify_input_string('09-input.txt')]
    
    # Part 1 -- answer 2662308295
    comp = Computer()
    comp.load_program(program=program)
    print(f"\nPart 1: {comp.run_program(inputs=[1])}")

    # Part 2
    comp = Computer()
    comp.load_program(program=program)
    print(f"\nPart 2: {comp.run_program(inputs=[2])}")