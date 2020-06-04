class Computer:
    """ An Intcode Computer. """

    def __init__(self):
        self.opcodes = [99, 1, 2, 3, 4, 5, 6, 7, 8]
        # self.system  = system  #
        self.program = None


    def run_program(self, program, noun=None, verb=None, inputs=[]):
        """ Runs the opcodes. """

        # Perform setup opertions
        self.program = program
        # self._set_system()
        if noun:
            self.program[1] = noun
        if verb:
            self.program[2] = verb

        # Run each opcode
        i, j = 0, 0  # i is the program index; j is the inputs index
        while i < len(program):
            opcode = self._get_opcode(i)
            # exit early
            if opcode == 99:
                self.program = None
                print("End of Line")
                return output

            params = self._get_exe_params(i)

            if opcode == 1:
                self.program[params[2]] = self.program[params[0]] + self.program[params[1]]
                i += 4

            elif opcode == 2:
                self.program[params[2]] = self.program[params[0]] * self.program[params[1]]
                i += 4

            elif opcode == 3:
                if inputs:
                    self.program[params[0]] = inputs[j]
                    j += 1
                else:
                    self._do_input(params)
                i += 2

            elif opcode == 4:
                # print("\nInstruction:", i)
                output = self.program[params[0]]
                print("Value:", output)
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
        print("    A single digit from 0 thru 4 for an Amplifier Phase Setting")
        print("    An Amplifier Output Signal for an Amplifier Input Signal (or '0')")
        
        value = input("Input please: ")
        # TODO: Add try/except for int(value)
        value = int(value)

        self.program[params[0]] = value  # self.system


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
