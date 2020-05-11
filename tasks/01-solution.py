""" Part 1 """
def calc_fuel_requirement(puzzle_input='01-input.txt'):
    # if mass < 6 ??

    total = 0

    with open(puzzle_input) as file:
        masses = file.readlines()

    for mass in masses:
        total += int(mass) // 3 - 2

    return total


""" Part 2 """
def get_modules(puzzle_input='01-input.txt'):

    with open(puzzle_input) as file:
        lines = file.readlines()

    return [int(line) for line in lines]


def calc_fuel_requirement_addl():

    modules = get_modules()

    total = 0
    for module in modules:
        total += calc_fuel(module)

    return total


def calc_fuel(mass):
    """ Recursive function to get the fuel needed for the mass of the fuel needed.

        A module of mass 14 requires 2 fuel. This fuel requires no further fuel
        (2 divided by 3 and rounded down is 0, which would call for a negative
        fuel), so the total fuel required is still just 2.
        At first, a module of mass 1969 requires 654 fuel. Then, this fuel
        requires 216 more fuel (654 / 3 - 2). 216 then requires 70 more fuel,
        which requires 21 fuel, which requires 5 fuel, which requires no further
        fuel. So, the total fuel required for a module of
        mass 1969 is 654 + 216 + 70 + 21 + 5 = 966.
        The fuel required by a module of mass 100756 and its fuel is:
        33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346.
    """

    if mass < 9:
        return 0

    fuel = mass // 3 - 2
    fuel += calc_fuel(fuel)

    return fuel

