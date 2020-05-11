import common

""" Part 1 """
def calc_fuel_requirement():
    # if mass < 6 ??

    masses = common.listify_input_file('01-input.txt')

    total = 0
    for mass in masses:
        total += int(mass) // 3 - 2

    return total


""" Part 2 """
def calc_fuel_requirement_addl():

    modules = common.listify_input_file('01-input.txt')

    total = 0
    for module in modules:
        total += calc_fuel(int(module))

    return total


def calc_fuel(mass):
    """ Recursive function to get the fuel needed for the mass of the fuel needed.

        A module of mass 14 requires 2 fuel. This fuel requires no further fuel
        (2 divided by 3 and rounded down is 0, which would call for a negative
        fuel), so the total fuel required is still just 2.
        >>> calc_fuel(14)
        2

        At first, a module of mass 1969 requires 654 fuel. Then, this fuel
        requires 216 more fuel (654 / 3 - 2); 216 then requires 70 more fuel,
        which requires 21 fuel, which requires 5 fuel, which requires no further
        fuel. The total for mass 1969 is 654 + 216 + 70 + 21 + 5 = 966.
        >>> calc_fuel(1969)
        966

        The fuel required by a module of mass 100756 and its fuel is:
        33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346.
        >>> calc_fuel(100756)
        50346
    """

    if mass < 9:
        return 0

    fuel = mass // 3 - 2
    fuel += calc_fuel(fuel)

    return fuel

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

