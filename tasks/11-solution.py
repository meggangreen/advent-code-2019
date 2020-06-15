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
        color = "white" if self.color == 1 else "black"
        painted = "painted" if self.been_painted == True else "not painted"
        return f"<Panel @ {self.coords} - {color} - {painted}>"


    def _be_painted(self, color):
        self.color = color
        self.been_painted = True


class Painter(Computer):
    
    def __init__(self):
        super().__init__()
        self.coords = 0+0j
        self.orientations = "^>V<"
        self.panels = dict()


    def __repr__(self):
        return f"<Painter @ {self.coords} {self.orientations[0]}>"


    def paint_all_panels(self):
        while True:
            self._register_panel()
            curr_color = self._photograph_panel()

            new_color, direction = self.run_program(inputs=[curr_color])
            if new_color is None or direction is None:
                print("End of Line")
                return

            if curr_color != new_color:
                self._paint_panel(new_color)
            self._turn(direction)
            self._advance()


    def _turn(self, direction):
        """ Shifts string of orientations left or right. """

        if direction == 0:
            self.orientations = self.orientations[3] + self.orientations[:3]
        else:
            self.orientations = self.orientations[1:] + self.orientations[0]


    def _advance(self):
        """ Changes coordinates based on orientation; called after _turn. """

        if self.orientations[0] == "^":
            self.coords += 1j
        elif self.orientations[0] == "v":
            self.coords += -1j
        elif self.orientations[0] == ">":
            self.coords += 1
        elif self.orientations[0] == "<":
            self.coords += -1


    def _register_panel(self):
        """ Ensures panel is registered. """

        if self.coords not in self.panels:
            self.panels[self.coords] = Panel(self.coords)


    def _photograph_panel(self):
        return self.panels[self.coords].color


    def _paint_panel(self, color):
        self.panels[self.coords]._be_painted(color)


##########
if __name__ == "__main__":
    program = [int(n) for n in common.listify_input_string('09-input.txt')]

    painter = Painter()
    painter.load_program(program=program)
