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

# big thing for me, in particular, to remember is we don't care *which* asteroid
# on the slope we count, just that we count *only one*

# PART 2 NOTES
# - get all unique slopes once
# - vaporize order is clockwise from 12; 
#       ergo slope order is above -> R-largest to R-mallest -> 
#                           below -> L-largest to L-smallest
# x get unique slopes *with* asteroid's distance: slopes = {slope: [diff_x+diff_y*1j]}
# x for each slope in slopes, sort asteroids lists farther-to-closer
#       sorted([asteroids], key=lambda A: abs(A.real)+abs(A.imag), reverse=True)
# x diff ways to fudge slope order
# - vaporized = 0; while vaporized < 200, 
#       for each slope in "ordered" slopes,
#           if slopes[slope]
#           target = slopes[slope].pop())
#           vaporized += 1
# 

import common
from operator import itemgetter

def make_asteroids(graph):
    """ Makes a generator of asteroids in a graph.

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


def get_slope(orig, dest):
    """ Returns the complex slope (side-slope) of the line connecting two asteroids.

    Args:
        orig (complex): an asteroid with location as 'x+yj'
        dest (complex): an asteroid with location as 'x+yj'

    Returns:
        string: a string describing the orientation and slope of a line;
                'above' or 'below' for vertical lines;
                'L 0.25' or 'R -3.0' are examples

    >>> get_slope(0, 3+2j)
    ('R', -0.6666666666666666)

    >>> get_slope(4-2j, -2+1j)
    ('L', 0.5)
    """
    
    if orig == dest:
        return None

    # slope is undefined (asteroids are in vertical path)
    if orig.real == dest.real:
        return ("Neath", float('-inf')) if orig.imag < dest.imag else ("Top", float('inf'))

    # dest is to R or L of orig
    side = "R" if orig.real < dest.real else "L"
    slope = (orig.imag - dest.imag) / -(orig.real - dest.real)

    return (side, slope)


def get_unique_slopes(orig, asteroids):
    """ Returns set of unique complex slopes from one origin asteroid to many
        destination asteroids.

    Args:
        orig (complex): an asteroid with location as 'x+yj'
        asteroids (iterable): iterable of many asteroids as complex numbers

    Returns:
        set: set of slopes as defined in `get_slope(o, d)`

    >>> graph = [".#..#",".....","#####","....#","...##"]
    >>> asteroids = make_asteroids(graph)
    >>> slopes = get_unique_slopes(1+0j, asteroids)
    >>> slopes == {('L', 2.0), ('R', -1.3333333333333333), ('R', 0.0), ('R', -0.6666666666666666), ('R', -1.0), ('R', -2.0), ('Neath', -inf)}
    True
    """

    slopes = set()

    for dest in asteroids:
        if orig != dest:
            slopes.add(get_slope(orig, dest))

    return slopes


def map_asteroids_to_slopes(orig, asteroids):
    """ Returns dict of all slopes and the distances to each asteroid along them.

    Args:
        orig (complex): asteroid coord
        asteroids (iterable): many asteroid coords

    Returns:
        dict: key: slope as define in `get_slope(orig, dest)`;
              val: list of x-y distances from orig as complex number
    """

    slopes = dict()

    for dest in asteroids:
        if orig != dest:
            slope = get_slope(orig, dest)
            if slope not in slopes:
                slopes[slope] = []
            slopes[slope].append(dest)

    return slopes


def vaporize_asteroids(monitor, asteroids):

    slopes = map_asteroids_to_slopes(monitor, asteroids)
    for slope in slopes:
        if len(slopes[slope]) > 1:
            slopes[slope] = sorted(slopes[slope], key=lambda A: abs(A.real-monitor.real)+abs(A.imag-monitor.imag), reverse=True)
    ordered_slopes = list(slopes.keys())
    ordered_slopes.sort(key=itemgetter(0,1), reverse=True)

    vaporized = []
    for slope in ordered_slopes:
        if slopes[slope]:
            vaporized.append(slopes[slope].pop())

    return vaporized


def do_part_1():
    """ Which asteroid can see the most other asteroids? """

    graph = common.listify_input_file("10-input.txt")
    asteroids = {asteroid: None for asteroid in make_asteroids(graph)}

    for asteroid in asteroids:
        asteroids[asteroid] = get_unique_slopes(asteroid, asteroids)

    return len(max(asteroids.items(), key=lambda item: len(item[1]))[1])


def do_part_2():
    """ Which asteroid is the 200th to be vaporized? """

    graph = common.listify_input_file("10-input.txt")
    asteroids = list(make_asteroids(graph))
    monitor = 17+22j  # answer from part 1
    vaporized = vaporize_asteroids(monitor, asteroids)

    return vaporized[199]


##########
if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)  # verbose=True

# Part 1:
print(f"Part 1: {do_part_1()}")  # answer 288 (17+22j)
print(f"Part 2: {do_part_2()}")  # answer 616 (6+16j)

