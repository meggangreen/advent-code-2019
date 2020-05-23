""" Parameters

[a,b,c,d,a,b,c,d ...]

a = action
b, c = actor address
d = result address

opcodes: 1  +
         2  *
         3  saves input to address
         4  returns value at address
         99 halt

params:  0  position -- value stored at position n
         1  immediate -- value is n

    "Parameters that an instruction writes to will never be in immediate mode."
    opcodes 1 & 2 have 3 params, 3rd param is always 0
    opcode 3 has 1 param, it is always 0
    opcode 4 has 1 param, could be 0 or 1

"""

import common
from copy import deepcopy

class Computer:

    def __init__(self):
        self.opcodes = [99, 1, 2, 3, 4]
        self.curr_program = None


    def run_program(self, program, noun=None, verb=None):
        """ Runs the opcodes. """

        # Perform setup opertions
        self.curr_program = program
        # self._set_system()
        if noun:
            self.curr_program[1] = noun
        if verb:
            self.curr_program[2] = verb

        # Run each opcode
        i = 0 
        while i < len(program):
            opcode, pmodes = self._extract_opcode_pmodes(program[i])

            # exit early
            if opcode == 99:
                print("End of Line")
                return

            if opcode == 1:
                self._do_addition(i, pmodes)
                i += 4

            elif opcode == 2:
                self._do_multiplication(i, pmodes)
                i += 4

            elif opcode == 3:
                self._do_input(i, pmodes)
                i += 2

            elif opcode == 4:
                self._do_output(i, pmodes)
                i += 2
                
            else:
                return "err: ", i

        return


    def _do_addition(self, i, pmodes):
        """ Execute addition operation. """

        params = [self.curr_program[i+1],
                  self.curr_program[i+2],
                  self.curr_program[i+3]]
        
        # Set values
        value0 = self.curr_program[params[0]] if pmodes[0] == 0 else params[0]
        value1 = self.curr_program[params[1]] if pmodes[1] == 0 else params[1]

        # Place result (pmodes[2] is always 0 for addition)
        self.curr_program[params[2]] = eval('value0 + value1')

        return None


    def _do_multiplication(self, i, pmodes):
        """ Execute multiplication operation. """

        params = [self.curr_program[i+1],
                  self.curr_program[i+2],
                  self.curr_program[i+3]]
        
        # Set values
        value0 = self.curr_program[params[0]] if pmodes[0] == 0 else params[0]
        value1 = self.curr_program[params[1]] if pmodes[1] == 0 else params[1]

        # Place result (pmodes[2] is always 0 for multiplication)
        self.curr_program[params[2]] = eval('value0 * value1')

        return None


    def _do_input(self, i, pmodes):
        """ Asks user for input. """

        params = [self.curr_program[i+1]]
        
        print("For the first input, enter the system ID:")
        print("    '1' for the Air Conditioner Unit")
        print("    '5' for the Thermal Radiator Controller")
        print("For all others, there is probably *an issue*. Cheers!")
        if i != 0:
            print("current instruction is", i)
        value0 = input("Input please: ")
        if value0 not in '15':
            # Raise error
            pass
        value0 = int(value0)

        # Place result (pmodes[0] is always 0 for input)
        self.curr_program[params[0]] = value0

        return None


    def _do_output(self, i, pmodes):
        """ Prints output. """

        params = [self.curr_program[i+1]]
        value0 = self.curr_program[params[0]] if pmodes[0] == 0 else params[0]

        # TODO - use string interpolation here
        print("\nInstruction:", i)
        print("Value:", value0)


    def _do_jump_if_true(self, i, pmodes):
    

    def _extract_opcode_pmodes(self, command):
        """ Returns opcode and pmodes for a given program command.

        Arguments:
            command {integer} -- One value from the list `program`

        Returns:
            integer -- opcode; must be one of: 1, 2, 3, 4, 99
            list -- pmodes; must contain only 0s and 1s; must be length 0, 1, or 3

        >>> comp._extract_opcode_pmodes(1002)
        (2, [0, 1, 0])

        >>> comp._extract_opcode_pmodes(1003)
        (3, [0])

        >>> comp._extract_opcode_pmodes(1101)
        (1, [1, 1, 0])

        >>> comp._extract_opcode_pmodes(99)
        (99, [])

        >>> comp._extract_opcode_pmodes(7)
        (99, [])

        >>> comp._extract_opcode_pmodes(1104)
        err: too many pmodes for opcode 4
        (4, [1])

        """

        opcode = int(str(command)[-2:])
        opcode = 99 if opcode not in self.opcodes else opcode

        pmodes = [int(n) for n in list(str(command)[:-2])][::-1]
        if opcode == 99:
            return (opcode, [])

        if opcode == 3:
            pmodes = [0]
        elif opcode == 4:
            if len(pmodes) < 1:
                pmodes.append(0)
            elif len(pmodes) > 1:
                print("err: too many pmodes for opcode", opcode)
                pmodes = [pmodes[0]]
        else:
            while len(pmodes) < 3:
                pmodes.append(0)       

        return (opcode, pmodes)

        
##########
if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={'comp': Computer()})  # https://stackoverflow.com/a/3936125

    program = [int(item) for item in common.listify_input_string('05-input.txt')]
    comp = Computer()
    
    # Part 1 -- starting input 1 for AC unit
    comp.run_program(program)  # answer 16434972
