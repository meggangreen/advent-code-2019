""" Parameters

[a,b,c,d,a,b,c,d ...]

a = action
b, c = actor address
d = result address

opcodes: 1  +
         2  *
         3  saves input to address
         4  returns value at address
         5  changes index if not 0
         6  changes index if 0
         7  stores 1 in p3 if p1 < p2, else 0
         8  stores 1 in p3 if p1 == p2, else 0
         99 halt/exit

params:  0  position -- value stored at position n
         1  immediate -- value is n

    "Parameters that an instruction writes to will never be in immediate mode."
    opcodes 1 & 2 have 3 params, 3rd param is always 0
    opcode 3 has 1 param, it is always 0
    opcode 4 has 1 param, could be 0 or 1

"""

import common

class Computer:

    def __init__(self):
        self.opcodes = [99, 1, 2, 3, 4, 5, 6, 7, 8]
        self.program = None


    def run_program(self, program, noun=None, verb=None):
        """ Runs the opcodes. """

        # Perform setup opertions
        self.program = program
        # self._set_system()
        if noun:
            self.program[1] = noun
        if verb:
            self.program[2] = verb

        # Run each opcode
        i = 0 
        while i < len(program):
            opcode = self._get_opcode(i)
            # exit early
            if opcode == 99:
                self.program = None
                print("End of Line")
                return

            params = self._get_exe_params(i)

            if opcode == 1:
                self.program[params[2]] = self.program[params[0]] + self.program[params[1]]
                i += 4

            elif opcode == 2:
                self.program[params[2]] = self.program[params[0]] * self.program[params[1]]
                i += 4

            elif opcode == 3:
                self._do_input(params)
                i += 2

            elif opcode == 4:
                print("\nInstruction:", i)
                print("Value:", self.program[params[0]])
                i += 2
                
            elif opcode == 5:
                if self.program[params[0]] != 0:
                    i = self.program[params[1]]
                else:
                    i += 3
                
            elif opcode == 6:
                if self.program[params[0]] == 0:
                    i = self.program[params[1]]
                else:
                    i += 3

            elif opcode == 7:
                if self.program[params[0]] < self.program[params[1]]:
                    self.program[params[2]] = 1
                else:
                    self.program[params[2]] = 0
                i += 4     

            elif opcode == 8:
                if self.program[params[0]] == self.program[params[1]]:
                    self.program[params[2]] = 1
                else:
                    self.program[params[2]] = 0
                i += 4
            
            else:
                return "err: ", i

        return


    def _do_input(self, params):
        """ Asks user for input. """
        
        print("For the first input, enter the system ID:")
        print("    '1' for the Air Conditioner Unit")
        print("    '5' for the Thermal Radiator Controller")
        # print("For all others, there is probably *an issue*. Cheers!")
        # if i != 0:
        #     print("current instruction is", i)
        value0 = input("Input please: ")
        if value0 not in '15':
            # Raise error
            pass
        value0 = int(value0)

        # Place result (pmodes[0] is always 0 for input)
        self.program[params[0]] = value0


    def _get_opcode(self, i):
        """ Returns opcode.
        
        Arguments:
            i {integer} -- Index of the command in `program`

        Returns:
            integer -- opcode; must be one of self.opcodes.

        """

        opcode = int(str(self.program[i])[-2:])
        return 99 if opcode not in self.opcodes else opcode


    def _get_exe_params(self, i):
        """ Make proper parameters based on parameter mode.

        Arguments:
            i {integer} -- Index of the command in `program`

        Returns:
            list -- list of executable command parameters

        """

        pmodes = [int(n) for n in list(str(self.program[i])[:-2])][::-1]
        while len(pmodes) < 3:
            pmodes.append(0)

        params = []
        params.append(self.program[i+1] if pmodes[0] == 0 else (i + 1))
        params.append(self.program[i+2] if pmodes[1] == 0 else (i + 2))
        params.append(self.program[i+3] if pmodes[2] == 0 else (i + 3))

        return params

        
##########
if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={'comp': Computer()})  # https://stackoverflow.com/a/3936125

    program = [int(item) for item in common.listify_input_string('05-input.txt')]
    comp = Computer()
    
    # Part 1 -- starting input 1 for AC unit -- answer 16434972
    # Part 2 -- starting input 5 for TRC -- answer 16694270
    comp.run_program(program)  

