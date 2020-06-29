""" Day 13 - an intcode computer day """

""" Notes

    - i'm not sure how complex the modeling needs to get, so for now i'll make
      only a screen snapshot.

"""

import common
from computer import Computer
from copy import deepcopy

TEST_SNAP_1 = [1, 2, 3, 6, 5, 4]
PROGRAM = [int(item) for item in common.listify_input_string('13-input.txt')]

def play_game(program, inputs=[]):

    comp = Computer()
    comp.load_program(program=program, system="game", inputs=inputs)
    comp.run_program()

    return comp


def parse_game_progression(progression):

    score = 0
    snapshot = dict()

    t = 2
    while t < len(progression):
        x = progression[t-2]
        y = progression[t-1]
        info = progression[t]
        if x == -1 and y == 0:
            score = info
        else:
            coord = x + y * 1j
            snapshot[coord] = info
        t += 3
    
    return (score, snapshot)


def count_block_tiles(snapshot):
    return list(snapshot.values()).count(2)


def do_part_one():
    game = play_game(PROGRAM)
    progression = game.outputs
    _, snapshot = parse_game_progression(progression)
    
    return count_block_tiles(snapshot)


def do_part_two():
    
    # Memory address 0 represents the number of quarters that have been
    # inserted; set it to 2 to play for free.
    program = deepcopy(PROGRAM)
    program[0] = 2

    game = Computer()
    game.load_program(program=program, system="game-auto")
    game.run_program()
    


##########
if __name__ == "__main__":
    # Part 1 -- answer 462
    print(f"Part 1: {do_part_one()}")

    # Part 2 -- answer 23981
    # Hints suggest that I actually have to play the game instead of finding the
    # scoring pattern. Or rather, the paddle has to follow the ball around.
    # Also, look into pygame?
