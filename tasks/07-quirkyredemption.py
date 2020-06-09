""" https://github.com/quirkyredemption/aoc2019/blob/master/aoc_day7.py """

from itertools import permutations

class IntCodeComputer:
    def __init__(self, program, setting):
        self.code = program
        self.inputs = [setting]
        self.index = 0

    def __repr__(self):
        return f"<QR inputs: {self.inputs}; >"

    def get_opcode(self):
        return self.code[self.index] % 100
    
    def get_modes(self):
        mode1 = (self.code[self.index] // 100) % 10
        mode2 = (self.code[self.index] // 1000) % 10
        mode3 = (self.code[self.index] // 10000) % 10
        return mode1, mode2, mode3

    def get_parameter(self, opcode):
        mode1, mode2, mode3 = self.get_modes()
        parameter1, parameter2, parameter3 = None, None, None

        if opcode in (1, 2, 7, 8):
            parameter1 = self.index + 1 if mode1 == 1 else self.code[self.index + 1]
            parameter2 = self.index + 2 if mode2 == 1 else self.code[self.index + 2]
            # the line below used to read ... self.index + 1 ... -- it works both ways
            parameter3 = self.index + 3 if mode3 == 1 else self.code[self.index + 3]
        elif opcode in (3, 4):
            parameter1 = self.index + 1 if mode1 == 1 else self.code[self.index + 1]
        elif opcode in (5, 6):
            parameter1 = self.index + 1 if mode1 == 1 else self.code[self.index + 1]
            parameter2 = self.index + 2 if mode2 == 1 else self.code[self.index + 2]
    
        return parameter1, parameter2, parameter3
    
    def run(self, inputs):
        self.inputs += inputs

        while self.index < len(self.code):
            opcode = self.get_opcode()
            parameter1, parameter2, parameter3 = self.get_parameter(opcode)

            if opcode == 1:
                self.code[parameter3] = self.code[parameter1] + self.code[parameter2]
            elif opcode == 2:
                self.code[parameter3] = self.code[parameter1] * self.code[parameter2]
            elif opcode == 3:
                self.code[parameter1] = self.inputs.pop(0)
            elif opcode == 4:
                self.index += 2
                output = self.code[parameter1]
                return output
            elif opcode == 5:
                self.index = self.code[parameter2] if self.code[parameter1] != 0 else self.index + 3
            elif opcode == 6:
                self.index = self.code[parameter2] if self.code[parameter1] == 0 else self.index + 3
            elif opcode == 7:
                self.code[parameter3] = int(self.code[parameter1] < self.code[parameter2])
            elif opcode == 8:
                self.code[parameter3] = int(self.code[parameter1] == self.code[parameter2])
            else:
                assert opcode == 99
                break

            if opcode in (1, 2, 7, 8):
                self.index += 4
            elif opcode == 3:
                self.index += 2


def amplificer(code, feedback):
    outputs = []

    if not feedback:
        sequence = permutations(range(5))
    elif feedback:
        sequence = permutations(range(5,10))
    
    for settings in sequence:
        # amps = []
        # s = 0
        # for setting in settings:
        #     s += 1
        #     name = str(settings) + "::" + str(setting) + "::" + str(s)
        #     amp = IntCodeComputer(name, code, setting)
        #     amps.append(amp)
        amps = [IntCodeComputer(code, setting) for setting in settings]

        output = 0

        if not feedback:
            for amp in amps:
                output = amp.run([output])
            outputs.append(output)
        elif feedback:
            while output is not None:
                outputs.append(output)
                for amp in amps:
                    output = amp.run([output])
    
    return max(outputs)


code = [int(x) for x in open("07-input.txt", "r").read().split(",")]
part1_answer = amplificer(code, False)
part2_answer = amplificer(code, True)

print(f"Maximum thruster output without feedback is {part1_answer}")
print(f"Maximum thruster output with feedback is {part2_answer}")