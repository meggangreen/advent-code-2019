""" https://gist.github.com/wmute/1671e16430347ca28d092ea2d4726950 """

# from intcode import Machine
from enum import Enum

class Machine:
    """Represents our intcode computer."""

    def __init__(self, registers, inputs):
        self.position = 0
        self.base = 0
        self.inputs = inputs
        self.outputs = []
        self.registers = dict(zip(range(len(registers)), registers))
        self.running = True
        self.halt = False

    def run(self):
        p = self.position
        (opcode, x, y, k) = [self.registers.get(i, 0) for i in range(p, p + 4)]
        (a, b, c, d, e) = [int(c) for c in str(opcode).rjust(5, "0")]
        # get values
        m = self.get_param(c, x)
        n = self.get_param(b, y)
        o = self.set_param(a, k)
        # process instructions
        if e == 1:
            self.registers[o] = m + n
            self.position += 4
        if e == 2:
            self.registers[o] = m * n
            self.position += 4
        if e == 3:
            self.registers[o] = self.inputs.pop(0)
            self.position += 2
        if e == 4:
            self.outputs.append(m)
            self.position += 2

            if len(self.outputs) == 2:
                self.running = False
        if e == 5:
            self.position = n if m != 0 else self.position + 3
        if e == 6:
            self.position = n if m == 0 else self.position + 3
        if e == 7:
            self.registers[o] = 1 if m < n else 0
            self.position += 4
        if e == 8:
            self.registers[o] = 1 if m == n else 0
            self.position += 4
        if e == 9:
            if d == 9:
                self.halt = True
                self.running = False
            else:
                self.base += self.get_param(c, x)
                self.position += 2

    def get_param(self, mode, value):
        if mode == 0:
            return self.registers.get(value, 0)
        if mode == 1:
            return value
        if mode == 2:
            return self.registers[value + self.base]

    def set_param(self, mode, value):
        if mode == 0 or mode == 1:
            return value
        if mode == 2:
            return self.base + value


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Robot:
    """Represents our robot."""

    def __init__(self):
        self.direction = Direction.UP
        self.position = Position(0, 0)
        self.turn_left = {
            Direction.UP: Direction.LEFT,
            Direction.LEFT: Direction.DOWN,
            Direction.DOWN: Direction.RIGHT,
            Direction.RIGHT: Direction.UP,
        }
        self.turn_right = {
            Direction.UP: Direction.RIGHT,
            Direction.LEFT: Direction.UP,
            Direction.DOWN: Direction.LEFT,
            Direction.RIGHT: Direction.DOWN,
        }

    def move(self):
        if self.direction == Direction.UP:
            self.position.x -= 1
        if self.direction == Direction.RIGHT:
            self.position.y += 1
        if self.direction == Direction.DOWN:
            self.position.x += 1
        if self.direction == Direction.LEFT:
            self.position.y -= 1

    def turn(self, direction):
        if direction == 1:
            self.direction = self.turn_right[self.direction]
        if direction == 0:
            self.direction = self.turn_left[self.direction]


with open("11-input.txt", "r") as infile:
    # challenge inputs
    data = infile.read().strip().split(",")
    arr = [int(x) for x in data]
    # computer and robot
    machine = Machine(arr, [1])
    robot = Robot()
    panels = {(0, 0): 0}
    # run simulation
    while not machine.halt:
        while machine.running:
            machine.run()

        if machine.halt:
            continue
        (new_color, new_direction) = machine.outputs
        # paint panel
        panels[(robot.position.x, robot.position.y)] = new_color
        robot.turn(new_direction)
        robot.move()
        # continue machine process
        machine.outputs = []
        machine.inputs.append(panels.get((robot.position.x, robot.position.y), 0))
        machine.running = True
        machine.run()

    print(len(panels)) # <--- part 1

    # part 2
    min_x = min([x[0] for x in panels.keys()])
    max_x = max([x[0] for x in panels.keys()])
    min_y = min([x[1] for x in panels.keys()])
    max_y = max([x[1] for x in panels.keys()])

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            p = "#" if panels.get((x, y), 0) == 1 else " "
            print(p, end="")
        print()