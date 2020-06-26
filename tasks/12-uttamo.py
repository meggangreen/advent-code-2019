""" https://gist.github.com/uttamo/67fb87c06dffbb5c499ab360bb7c3b51 """

import unittest
from typing import List
# import os.path

import numpy as np


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'Vector({self.x}, {self.y}, {self.z})'

    def __str__(self):
        return f'<x={self.x}, y={self.y}, z={self.z}>'

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def energy(self):
        return sum(abs(v) for v in (self.x, self.y, self.z))


class MotionCalculator:
    def __init__(self, filename: str):
        self.filename = filename
        self.positions = self.load_data_from_file()
        self.velocities = [Vector(0, 0, 0) for _ in range(4)]
        self.history = {'x': set(), 'y': set(), 'z': set()}
        self.repeating_numbers = {'x': None, 'y': None, 'z': None}
        self.current_step_number = 0

    def load_data_from_file(self) -> List[Vector]:
        with open(self.filename, 'r') as inp:
            data = inp.read()
        positions = []
        for line in data.split('\n'):
            dim_value_pairs = [i.strip() for i in line[1:-1].split(',')]
            x, y, z = [int(i.split('=')[1]) for i in dim_value_pairs]
            positions.append(Vector(x, y, z))
        return positions

    def step_n_times(self, n: int):
        for _ in range(n):
            self.step()

    def step(self):
        # Calculate velocities
        x_positions = []
        y_positions = []
        z_positions = []

        for i_moon, position_vec in enumerate(self.positions):
            x_positions.append((i_moon, position_vec.x))
            y_positions.append((i_moon, position_vec.y))
            z_positions.append((i_moon, position_vec.z))

        sorting_key = lambda x: x[1]
        x_positions = sorted(x_positions, key=sorting_key)
        y_positions = sorted(y_positions, key=sorting_key)
        z_positions = sorted(z_positions, key=sorting_key)

        # Instantiate velocity change vectors
        velocity_changes = [Vector(0, 0, 0) for _ in range(4)]
        for dimension, position_list in [('x', x_positions),
                                         ('y', y_positions),
                                         ('z', z_positions)]:

            for i_moon, ordered_pos in position_list:
                number_greater = sum(pos > ordered_pos for _, pos in position_list)
                number_lesser = sum(pos < ordered_pos for _, pos in position_list)
                setattr(velocity_changes[i_moon], dimension, number_greater - number_lesser)

        # Update velocities
        for i_moon, velocity_change in enumerate(velocity_changes):
            self.velocities[i_moon] = self.velocities[i_moon] + velocity_change

        # Update positions
        for i_moon, velocity in enumerate(self.velocities):
            self.positions[i_moon] = self.positions[i_moon] + velocity

        self.current_step_number += 1

    def total_energy(self) -> int:
        total = 0
        for position, velocity in zip(self.positions, self.velocities):
            total += position.energy() * velocity.energy()

        return total

    def add_to_history(self) -> bool:
        # history_tuple = (tuple(self.positions), tuple(self.velocities))
        x_values = (tuple(v.x for v in self.positions), tuple(v.x for v in self.velocities))
        y_values = (tuple(v.y for v in self.positions), tuple(v.y for v in self.velocities))
        z_values = (tuple(v.z for v in self.positions), tuple(v.z for v in self.velocities))

        for dimension, values_tup in [('x', x_values),
                                      ('y', y_values),
                                      ('z', z_values)]:
            # if all repeating cycles have been found then stop
            if all(i for i in self.repeating_numbers.values()):
                return False
            if self.repeating_numbers[dimension] is None:
                if values_tup in self.history[dimension]:
                    # repeating cycle number found so store it
                    self.repeating_numbers[dimension] = self.current_step_number
                else:
                    self.history[dimension].add(values_tup)

        return True


def part1(filename: str, steps: int) -> int:
    calculator = MotionCalculator(filename)
    calculator.step_n_times(steps)
    return calculator.total_energy()


def part2(filename: str) -> int:
    calculator = MotionCalculator(filename)
    while True:
        if not calculator.add_to_history():
            return np.lcm.reduce(list(calculator.repeating_numbers.values()))
        calculator.step()


class TestSolutions(unittest.TestCase):
    def test_part1(self):
        # assert part1('inp1.txt', 10) == 179
        # assert part1('inp2.txt', 100) == 1940
        assert part1('12-input.txt', 1000) == 9127

    def test_part2(self):
        # assert part2('inp1.txt') == 2772
        # assert part2('inp2.txt') == 4_686_774_924
        assert part2('12-input.txt') == 353_620_566_035_124  # takes a long time


if __name__ == '__main__':
    unittest.main()
    # print(part2('12-input.txt'))