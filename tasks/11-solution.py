""" Day 11 """

""" Notes

    - Robot is a Computer that paints
    - "camera" provides input -- panel's current color
    - outputs (new color, turn direction)
        - paints panel output color
            0 black
            1 white
        - after turning moves forward to next panel
            0 left
            1 right

    - Panel is an object
        - has coords (x+yj)
        - has been painted or not
        - has color
        - stored in dict panels {coord: Panel}

"""

import common
from computer import Computer


