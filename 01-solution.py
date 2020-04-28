""" Part 1 """
def calc_fuel_requirement(puzzle_input):
    # if mass < 6 ??

    total = 0

    with open(puzzle_input) as file:
        masses = file.readlines()

    for mass in masses:
        total += int(mass) // 3 - 2

    return total

