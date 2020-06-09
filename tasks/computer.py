class Computer:
    """ An Intcode Computer. """

    def __init__(self):
        self.opcodes = [99, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.inputs  = []
        self.program = None


    def __repr__(self):
        return f"<Comp inputs: {self.inputs}; >"


    def load_program(self, program, noun=None, verb=None, system=None):
        """ Performs the setup operations. """

        self.program = program
        self.index = 0
        if noun is not None:
            self.program[1] = noun
        if verb is not None:
            self.program[2] = verb
        if system is not None:
            self.inputs.append(system)


    def run_program(self, inputs):
        """ Runs the opcodes. """

        self.inputs += inputs

        # Run each opcode
        while self.index < len(self.program):
            opcode = self._get_opcode()

            if opcode == 99:
                # self.program = None
                # print("End of Line")
                return None

            params = self._get_exe_params(opcode)

            # Addition
            if opcode == 1:
                self.program[params[2]] = self.program[params[0]] + self.program[params[1]]
                self.index += 4

            # Multiplication
            elif opcode == 2:
                self.program[params[2]] = self.program[params[0]] * self.program[params[1]]
                self.index += 4

            # Input
            elif opcode == 3:
                if inputs:
                    self.program[params[0]] = self.inputs.pop(0)
                else:
                    self._do_input(params)
                self.index += 2

            # Output
            elif opcode == 4:
                output = self.program[params[0]]
                # print(f"Opcode 4 outputting {output}")
                self.index += 2
                return output
                
            # Jump index not equal to zero ("if true")
            elif opcode == 5:
                if self.program[params[0]] != 0:
                    self.index = self.program[params[1]]
                else:
                    self.index += 3
                
            # Jump index equal to zero ("if false")
            elif opcode == 6:
                if self.program[params[0]] == 0:
                    self.index = self.program[params[1]]
                else:
                    self.index += 3

            # Is less than -- store 1 or 0
            elif opcode == 7:
                if self.program[params[0]] < self.program[params[1]]:
                    self.program[params[2]] = 1
                else:
                    self.program[params[2]] = 0
                self.index += 4     

            # Equals -- store 1 or 0
            elif opcode == 8:
                if self.program[params[0]] == self.program[params[1]]:
                    self.program[params[2]] = 1
                else:
                    self.program[params[2]] = 0
                self.index += 4

            # Jump relative base
            # elif opcode == 9:

        return


    def _do_input(self, params):
        """ Asks user for input. """
        
        print("For the first input, enter the system ID:")
        print("    '1' for the Air Conditioner Unit")
        print("    '5' for the Thermal Radiator Controller")
        print("    A single digit from 0 thru 4 for an Amplifier Phase Setting")
        print("    An Amplifier Output Signal for an Amplifier Input Signal (or '0')")
        
        value = input("Input please: ")
        # TODO: Add try/except for int(value)
        value = int(value)

        self.program[params[0]] = value  # system


    def _get_opcode(self):
        """ Returns opcode.
        
        Arguments:
            i {integer} -- Index of the command in `program`

        Returns:
            integer -- opcode; must be one of self.opcodes.

        """

        opcode = int(str(self.program[self.index])[-2:])
        return 99 if opcode not in self.opcodes else opcode


    def _get_exe_params(self, opcode):
        """ Makes proper parameters based on parameter mode.

        Arguments:
            i {integer} -- Index of the command in `program`

        Returns:
            list -- list of executable command parameters

        """

        pmodes = [int(n) for n in list(str(self.program[self.index])[:-2])][::-1]
        while len(pmodes) < 3:
            pmodes.append(0)

        params = [None, None, None]
        params[0] = self.index + 1 if pmodes[0] == 1 else self.program[self.index+1]

        if opcode in [1, 2, 5, 6, 7, 8]:
            params[1] = self.index + 2 if pmodes[1] == 1 else self.program[self.index+2]
        
        if opcode in [1, 2, 7, 8]:
            params[2] = self.index + 1 if pmodes[2] == 1 else self.program[self.index+3]

        return params
