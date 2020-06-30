class Computer:
    """ An Intcode Computer. """

    def __init__(self):
        self.opcodes = [99, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.system = None
        self.program = None
        self.inputs  = None
        self.outputs = None


    def __repr__(self):
        if 'game' in self.system:
            if self.outputs:
                self._render_screen()

        return f"<Comp inputs: {self.inputs}; >"


    def load_program(self, program, noun=None, verb=None, system=None, inputs=[]):
        """ Performs the setup operations. """

        self.program = program
        self.index = 0
        self.rel_base = 0
        self.inputs = []
        self.outputs = []
        if noun is not None:
            self.program[1] = noun
        if verb is not None:
            self.program[2] = verb
        if 'game' in system:
            self.system = system
        elif system is not None:
            self.inputs.append(system)
        self.inputs += inputs


    def run_program(self, inputs=[]):
        """ Runs the opcodes. """

        self.inputs += inputs

        # Run each opcode
        while self.index < len(self.program):
            opcode = self._get_opcode()

            if opcode == 99:
                # self.program = None
                # print("End of Line")
                if 'game' in self.system:
                    self._render_screen()
                return None

            params = self._get_exe_params(opcode)
            self._check_program_length(params)

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
                if self.inputs:
                    self.program[params[0]] = self.inputs.pop(0)
                elif self.system == "game-auto":
                    self.program[params[0]] = self._get_game_auto_input()
                elif self.system == "game-manual":
                    self.program[params[0]] = self._get_game_joystick_input()
                else:
                    self.program[params[0]] = self._get_regular_input(params)
                self.index += 2

            # Output
            elif opcode == 4:
                output = self.program[params[0]]
                # print(f"Opcode 4 outputting {output}")
                self.index += 2
                self.outputs.append(output)

                # # !Important! 
                # # Previous days' solutions require the output to be returned!
                # # Not required for: 13
                # return output
                
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
            elif opcode == 9:
                self.rel_base += self.program[params[0]]
                self.index += 2

        return


    def _get_regular_input(self, params):
        """ Asks user for input. """
        
        print("For the first input, enter the system ID:")
        print("    '1' for the Air Conditioner Unit")
        print("    '5' for the Thermal Radiator Controller")
        print("    A single digit from 0 thru 4 for an Amplifier Phase Setting")
        print("    An Amplifier Output Signal for an Amplifier Input Signal (or '0')")
        
        value = input("Input please: ")
        # TODO: Add try/except for int(value)
        value = int(value)

        return value  # system


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

        modes = [int(n) for n in list(str(self.program[self.index])[:-2])][::-1]
        while len(modes) < 3:
            modes.append(0)

        params = []

        if opcode:
            if modes[0] == 0:      # Relative mode
                params.append(self.program[self.index+1])
            elif modes[0] == 1:    # Immediate mode
                params.append(self.index + 1)
            elif modes[0] == 2:    # Relative mode
                params.append(self.rel_base + self.program[self.index+1])

        if opcode in [1, 2, 5, 6, 7, 8]:
            if modes[1] == 0:      # Relative mode
                params.append(self.program[self.index+2])
            elif modes[1] == 1:    # Immediate mode
                params.append(self.index + 2)
            elif modes[1] == 2:    # Relative mode
                params.append(self.rel_base + self.program[self.index+2])

        if opcode in [1, 2, 7, 8]:
            if modes[2] == 0:      # Relative mode
                params.append(self.program[self.index+3])
            elif modes[2] == 1:    # Immediate mode
                params.append(self.index + 1)
            elif modes[2] == 2:    # Relative mode
                params.append(self.rel_base + self.program[self.index+3])

        return params


    def _check_program_length(self, params):
        """ Checks the program length ("memory") is big enough. Calls method to
            increase length if necessary.
        """

        for param in params:
            current = len(self.program) - 1
            if param > current:
                self._extend_program_length(param - current)


    def _extend_program_length(self, extension):
        self.program += [0] * extension


    def _get_game_auto_input(self):

        snapshot = self._parse_game_progression()

        if snapshot['ball'].real < snapshot['paddle'].real:
            action = -1
        elif snapshot['ball'].real > snapshot['paddle'].real:
            action = 1
        else:
            action = 0

        return action
    
    
    def _get_game_joystick_input(self):
        """ Asks user for to move joystick L (-1), R (1), or to stay (0). """

        self._render_screen()
        
        directions = {'L': -1, 'S': 0, 'R': 1}
        
        print("Joystick Input:")
        print("    <-- L -- S -- R -->")
        print("    Enter 'L' for Left; 'S' to Stay, 'R' for Right")
        choice = input(">>> ").upper()

        if choice not in ['L', 'S', 'R']:
            choice = 'S'
            print("Invalid input. Staying put.")
        
        return directions[choice]


    def _parse_game_progression(self):

        snapshot = {"score": 0, "ball": -1-1j, "paddle": -1-1j}

        t = 2
        while t < len(self.outputs):
            x = self.outputs[t-2]
            y = self.outputs[t-1]
            info = self.outputs[t]
            if x == -1 and y == 0:
                snapshot['score'] = info
            else:
                coord = x + y * 1j
                snapshot[coord] = info
                if info == 4:
                    snapshot['ball'] = coord
                if info == 3:
                    snapshot['paddle'] = coord
            t += 3
        
        return snapshot


    def _render_screen(self):
        
        snapshot = self._parse_game_progression()

        coords = list(filter(lambda c: type(c) == complex, snapshot.keys()))
        max_x = max([int(c.real) for c in coords])
        max_y = max([int(c.imag) for c in coords])

        visualization = []
        for y in range(max_y+1):
            visualization.append("\n")
            for x in range(max_x+1):
                coord = x + y * 1j
                tile = snapshot.get(coord, 0)
                tile = tile if tile != 0 else ' '
                visualization.append(f"{tile}")
        
        visualization.append(f"\n\nScore: {snapshot['score']}\n")

        print(''.join(visualization))

