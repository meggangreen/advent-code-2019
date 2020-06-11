""" Day 10 """

# for one asteroid, i want to know it's line of sight to every other asteroid?
# for one asteroid, i want to follow a line of sight and cancel out blocked asteroids?

# it looks like lots of people used atan2 -- but idk what that is rn so i'm
# looking at a ruby solution that followed my second thought: get the slope of
# the line and cancel out other asteroids with that slope 

# notes from studying a ruby solution (https://github.com/J-Swift/advent-of-code-2019/blob/master/day_10/part_1/solution.rb)
# - it becomes important to note L and R sides of the asteroid for the slope
# - for the same reason, it's important to note above or below when ast1.x == ast2.x
# - other solutions talk about "floating point math"; is it necessary to keep as fraction (rational in ruby)?


import common

def make_asteroids(graph):
    """Makes a generator of asteroids in a graph.

    Args:
        graph (list of iterables): [description]

    Yields:
        complex: x, y coordinates represented as complex numbers; 
                 x is real, y is imaginary
    """

    for y, row in enumerate(graph):
        for x, char in enumerate(row):
            if char == '#':
                yield x + y * 1j


##########
if __name__ == "__main__":
    graph = common.listify_input_file("10-input.txt")
