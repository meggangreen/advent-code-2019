""" Parameters

    - find the taxicab (manhattan) distance of a gridpoint to 0,0
    - two wires; each has path in list of directions and units traveled
    - where do the two paths intersect?
    - which intersection is closest to 0,0?
    - how far from 0,0 is the closest intersection?

"""

import common as cmn

class Wire:
    def __init__(self, path, start=0+0j):
        self.start = start
        self.end = start
        self.path = path.split(",")
        self.coords = [start]

    def _make_coords(self):
        """ First coord is start; remaining coords are filled by walking path segments. """
        
        seg_coords = set()
        end = self.end

        for segment in self.path:
            d = segment[0]                      # direction UDRL
            sign = "+" if d in 'RU' else "-"    # positive or negative value
            j = "j" if d in "UD" else ""        # add j for y axis (imaginary)
            qty = int(segment[1:])              # total quantity to move

            seg_coords = [end + complex(sign + str(v) + j) for v in range(1, qty+1)]
            self.coords.extend(seg_coords)

            end = seg_coords[-1]  # new starting place

        self.end = end


def calc_distance(coord):
    """ Return coordinate (complex number) Taxi Distance from 0+0j. 
    
        >>> calc_distance(3+3j)
        6

        >>> calc_distance(-2+5j)
        7

    """
    return abs(coord.real) + abs(coord.imag)


def get_all_intersections(wire0, wire1):
    """ Returns a set of coordinates both wires cross. """
    return set(wire0.coords).intersection(set(wire1.coords))


def get_closest_intersection(wire0, wire1):
    x_set = get_all_intersections(wire0, wire1)
    distance = float('inf')
    closest_x = None
    for x in x_set:
        if x == 0+0j:
            continue
        x_distance = calc_distance(x)
        if x_distance < distance:
            closest_x = x
        distance = min(x_distance, distance)

    return (closest_x, distance)


def get_coordinate_index(wire, coord):
    for i, c in enumerate(wire.coords):
        if c == coord:
            return i
    return float('inf')


def get_fewest_steps_intersection(wire0, wire1):
    x_set = get_all_intersections(wire0, wire1)
    steps = float('inf')
    fewest_x = None
    for x in x_set:
        if x == 0+0j:
            continue
        x_steps = get_coordinate_index(wire0, x) + get_coordinate_index(wire1, x)
        if x_steps < steps:
            fewest_x = x
        steps = min(x_steps, steps)

    return (fewest_x, steps)


#########
if __name__ == '__main__':
    wires = cmn.listify_input_file('03-input.txt')

    wire0 = Wire(wires[0])
    wire0._make_coords()
    wire1 = Wire(wires[1])
    wire1._make_coords()
    print("test1:", get_closest_intersection(wire1, wire0))
    print("test2:", get_fewest_steps_intersection(wire1, wire0))

    wire0 = Wire(wires[-1])
    wire0._make_coords()
    wire1 = Wire(wires[-2])
    wire1._make_coords()

    print("Part 1:", get_closest_intersection(wire1, wire0))
    print("Part 2:", get_fewest_steps_intersection(wire1, wire0))
