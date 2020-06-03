""" This helped me understand the confusing instructions. But my ambition is to
    create something like kresimir-lukin (https://github.com/kresimir-lukin/AdventOfCode2019/blob/aa886874e34c3eb5d623ba3043496abd0fec8a26/intcode.py)
"""

# https://github.com/quirkyredemption/aoc2019/blob/master/aoc_day5.py
# AoC December 2nd Part 1
# file_path = r"PATH"

# opcodes = open(file_path, "r").read().split(",")
# opcodes = list(map(int, opcodes))

### MMG
import common
opcodes = [int(item) for item in common.listify_input_string('05-input.txt')]
# part 2 answer 16694270
###

intput = 5

def parameter_mode(opcodes, instruction, idx):
    instruction = list(str(instruction))
    
    paramter_modes = ([0]*(5-len(instruction))) + instruction
    
    param1_value = opcodes[idx + 1] if int(paramter_modes[2]) == 0 else (idx + 1)
    param2_value = (opcodes[idx + 2] if int(paramter_modes[1]) == 0 else (idx + 2))
    param3_value = (opcodes[idx + 3] if int(paramter_modes[0]) == 0 else (idx + 3))

    return param1_value, param2_value, param3_value

idx = 0
while idx < len(opcodes):
    instruction = opcodes[idx]
    opcode = int(str(instruction)[-1])
    param1, param2, param3 = parameter_mode(opcodes, instruction, idx)

    if opcode == 1:
        opcodes[param3] = opcodes[param1] + opcodes[param2]
        idx += 4
    
    if opcode == 2:
        opcodes[param3] = opcodes[param1] * opcodes[param2]
        idx += 4

    if opcode == 3:
        opcodes[param1] = intput
        idx += 2

    if opcode == 4 or opcode == 99:
        if opcodes[param1] != 0 and opcodes[idx + 2] == 99:
            print(f"Diagnostic tests succeed, final output = {opcodes[param1]}")
            break
        elif opcodes[param1] != 0 and opcodes[idx + 2] != 99:
            print(f"Diagnostic tests failed, output = {opcodes[param1]}")
            break
        else:
            print(f"Diagnostic test succeed, output = {opcodes[param1]}")
        idx += 2

    if opcode == 5: 
        if opcodes[param1] != 0:
            idx = opcodes[param2]
        else:
            idx += 3
        
    if opcode == 6:
        if opcodes[param1] == 0:
            idx = opcodes[param2]
        else:
            idx += 3

    if opcode == 7:
        if opcodes[param1] < opcodes[param2]:
            opcodes[param3] = 1
        else:
            opcodes[param3] = 0
        idx += 4     

    if opcode == 8:
        if opcodes[param1] == opcodes[param2]:
            opcodes[param3] = 1
        else:
            opcodes[param3] = 0
        idx += 4  
