import numpy as np
from lib.color_diff import *
from colormath.color_objects import LabColor

class Color:

    # cielab = [L, a, b]
    # color_proportions = { color1: 0.25, color2: 0.40, color3: 0.35 }
    
    def get_delta(self, other):
        color_lab = LabColor(self.cielab[0], self.cielab[1], self.cielab[2])
        other_lab = LabColor(other.cielab[0], other.cielab[1], other.cielab[2])
        #delta_e = delta_e_cie1976(color_lab, other_lab)
        delta_e = delta_e_cie2000(color_lab, other_lab)
        return delta_e

    def __init__(self, l, a, b, color_proportions=None):
        self.cielab = np.zeros(3)
        self.cielab[0] = l
        self.cielab[1] = a
        self.cielab[2] = b
        self.color_proportions = color_proportions

    def __hash__(self) -> int:
        return hash((self.cielab[0], self.cielab[1], self.cielab[2]))

    def __eq__(self, other: object) -> bool:
        return self.get_delta(other) == 0

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        if(self.color_proportions == None):
            return str(self.cielab)
        return '\n'.join([f'{key}: {round(value,4)}' for key, value in self.color_proportions.items()])

    def __repr__(self) -> str:
        return self.__str__()