""" Day 4 Parameters
    
    - It is a six-digit number.
    - The value is within the range given in your puzzle input.
    - Two adjacent digits are the same (like 22 in 122345).
    - Going from left to right, the digits never decrease

    examples (outside of range):
    - 111111 meets these criteria (double 11, never decreases).
    - 223450 does not meet these criteria (decreasing pair of digits 50).
    - 123789 does not meet these criteria (no double)


"""


PZL_IN = (264360, 746325)

def is_valid(pword):
    """ Determines if pword is valid against Part 1 criteria. """

    p_str = str(pword)
    has_double = False

    for i in range(len(p_str)-1):
        if p_str[i] > p_str[i+1]:
            return False
        if p_str[i] == p_str[i+1]:
            has_double = True

    return has_double


def get_valid_pwords(limits=PZL_IN):
    """ Returns list of valid passwords from range. """

    valid_pwords = []

    for pword in range(limits[0], limits[1]+1):
        valid_pwords.append(pword) if is_valid(pword) else False

    return valid_pwords


def new_is_valid(pword):
    """ Determines if pword is valid against Part 1 criteria. """

    p_str = str(pword)
    has_double = False

    i = 0
    while i < len(p_str)-1:
        recurs = 0
        for j in range(i+1, len(p_str)):
            if p_str[j] < p_str[i]:     # cannot decrease
                return False
            if p_str[j] != p_str[i]:    # end recurring number streak
                break
            else:
                recurs += 1
        has_double = True if recurs == 1 else has_double
        i = j

    return has_double


def get_new_valid_pwords(limits=PZL_IN):
    """ Returns list of valid passwords from range. """

    valid_pwords = []

    for pword in range(limits[0], limits[1]+1):
        valid_pwords.append(pword) if new_is_valid(pword) else False

    return valid_pwords


###########
if __name__ == '__main__':
    print("Part 1:", len(get_valid_pwords()))
    print("Part 2:", len(get_new_valid_pwords()))
