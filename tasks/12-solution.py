""" Day 12

    Notes:
    - Moon
        - 3D position (input)
            - position = old position + velocity
        - 3D velocity (starts at 0-0-0)
            - velocity = each moon's gravity acting on the others
        - Energy = potential * kinetic
            - potential = sum(abs(positions))
            - kinetic = sum(abs(velocities))

    - System energy = sum(moons' energies)

    - Q: What is the total system energy after 1000 time steps?
"""

from copy import deepcopy

TEST_MOONS_1 = "<x=-1, y=0, z=2>\n<x=2, y=-10, z=-7>\n<x=4, y=-8, z=8>\n<x=3, y=5, z=-1>"
TEST_MOONS_2 = "<x=-8, y=-10, z=0>\n<x=5, y=5, z=10>\n<x=2, y=-7, z=3>\n<x=9, y=-8, z=-3>"
MOONS = "<x=-8, y=-9, z=-7>\n<x=-5, y=2, z=-1>\n<x=11, y=8, z=-14>\n<x=1, y=-4, z=-11>"
NAMES = ["Io", "Eu", "Gn", "Cl"]

class Moon():
    AXES = 'xyz'

    def __init__(self, name, x, y, z):
        self.name = name
        self.position = {'x': x, 'y': y, 'z': z}
        self.velocity = {'x': 0, 'y': 0, 'z': 0}
        self.energy = {'p': None, 'k': None}
        self._calc_energy()

    def __repr__(self):
        return f"<{self.name} @ {self.position} : {self.velocity} : {self.energy} />"


    def step_in_time(self, static_moons):
        self._apply_gravity(static_moons)
        self._apply_velocity()
        self._calc_energy()

    
    def _calc_energy(self):
        self.energy['p'] = sum([abs(v) for v in self.position.values()])
        self.energy['k'] = sum([abs(v) for v in self.velocity.values()])


    def _apply_gravity(self, static_moons):
        for name, position in static_moons.items():
            if self.name == name:
                continue
            for axis in self.AXES:
                if self.position[axis] == position[axis]:
                    continue
                elif self.position[axis] > position[axis]:
                    self.velocity[axis] += -1
                elif self.position[axis] < position[axis]:
                    self.velocity[axis] += 1
    

    def _apply_velocity(self):
        for axis in self.AXES:
            self.position[axis] += self.velocity[axis]


def make_moons(data, names=NAMES):

    moons = dict()
    data = [c for c in [coord[1:-1].split(", ") for coord in data.split("\n")]]

    for i in range(len(names)):
        x, y, z = (int(c.split('=')[1]) for c in data[i])
        moons[names[i]] = Moon(names[i], x, y, z)

    return moons


def capture_static_moons(moons):
    
    return {moon.name: deepcopy(moon.position) for moon in moons.values()}


def test_set_1():
    data = TEST_MOONS_1
    moons = make_moons(data)

    print("\n\n")
    for moon in moons.values():
        print(moon)

    t = 0
    while t < 10:
        t += 1
        # print()
        static_moons = capture_static_moons(moons)
        for moon in moons.values():
            moon.step_in_time(static_moons)
            # print(moon)
    
    print("\n")
    for moon in moons.values():
        print(moon)


def test_set_2():
    data = TEST_MOONS_2
    moons = make_moons(data)

    print("\n\n")
    for moon in moons.values():
        print(moon)

    t = 0
    while t < 100:
        t += 1
        # if t % 10 == 0:
            # print()
        static_moons = capture_static_moons(moons)
        for moon in moons.values():
            moon.step_in_time(static_moons)
            # if t % 10 == 0:
                # print(moon)

    print("\n")
    for moon in moons.values():
        print(moon)


def do_part_1():
    data = MOONS
    moons = make_moons(data)

    # print("\n\n")
    # for moon in moons.values():
    #     print(moon)

    t = 0
    while t < 1000:
        t += 1
        # if t % 10 == 0:
            # print()
        static_moons = capture_static_moons(moons)
        for moon in moons.values():
            moon.step_in_time(static_moons)
            # if t % 10 == 0:
                # print(moon)

    # print("\n")
    sys_energy = 0
    for moon in moons.values():
        sys_energy += moon.energy['p'] * moon.energy['k']
        # print(moon)

    return sys_energy    
    

##########
if __name__ == "__main__":
    # test_set_1()
    # test_set_2()

    # Part 1 -- answer 9127
    print(f"Part 1: {do_part_1()}")

    # Part 2 -- answer 353620566035124
    # see 12-uttamo
    
