""" Day 11 """

""" Notes

    - Painter is a Computer that paints
        - has its current coords (could track path, but not necessary)
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
        return f"<Panel @ {self.coords} - {color} - {painted}>"


    def _be_painted(self, color):
        self.color = color
        self.been_painted = True


class Painter(Computer):
    
    def __init__(self):
        super().__init__()
        self.coords = 0+0j
        self.orientations = ("^", ">", "v", "<")
        self.panels = dict()


    def __repr__(self):
        return f"<Painter @ {self.coords} {self.orientations[0]}>"


    def _turn(self, direction):

        if direction == 0:
            self.orientations = self.orientations[3] + self.orientations[:3]
        else:
            self.orientations = self.orientations[1:] + self.orientations[0]


    def _advance(self):

        if self.orientations[0] == "^":
            self.coords += 1j
        elif self.orientations[0] == "v":
            self.coords += -1j
        elif self.orientations[0] == ">":
            self.coords += 1
        elif self.orientations[0] == "<":
            self.coords += -1
