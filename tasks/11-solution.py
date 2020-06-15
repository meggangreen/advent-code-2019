""" Day 11 """

""" Notes

    - Robot is a Computer that paints
        - registers and tracks panels
        - takes photos for input -- panel's current color
        - outputs (new color, turn direction)
            - paints panel output color
                0 black
                1 white
            - after turning moves forward to next panel
                0 left
                1 right
    - do not reload program

    - Panel is an object
        - has coords (x+yj)
        - has been painted or not
        - has color
        - stored in dict panels {coord: Panel}

"""

import common
from computer import Computer

class Panel(object):
    
    def __init__(self, coords):
        self.coords = coords
        self.color = 0
        self.been_painted = False

    def __repr__(self):
        color = "white" if self.color = 1 else "black"
        painted = "painted" if self.been_painted = True else "not painted"
        return f"<P @ {self.coords} - {color} - {painted}>"

    def _be_painted(self, color):
        self.color = color
        self.been_painted = True


