import numpy as np
from lib.color_diff import delta_e_cie2000
from colormath.color_objects import LabColor

class Color:

    # cielab = [L, a, b]
    # color_proportions = { color1: 0.25, color2: 0.40, color3: 0.35 }
    
    def get_delta(self, other):
        color_lab = LabColor(self.cielab[0], self.cielab[1], self.cielab[2])
        other_lab = LabColor(other.cielab[0], other.cielab[1], other.cielab[2])
        return delta_e_cie2000(color_lab, other_lab)

    def __init__(self, l, a, b, color_proportions=None):
        self.cielab = np.zeros(3)
        self.cielab[0] = l
        self.cielab[1] = a
        self.cielab[2] = b
        self.color_proportions = color_proportions

    def __hash__(self) -> int:
        return hash((self.cielab[0], self.cielab[1], self.cielab[2]))

    def __eq__(self, other: object) -> bool:
        return self.cielab == other.cielab

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __str__(self) -> str:
        return f"[ L: {self.cielab[0]}, a: {self.cielab[1]}, b: {self.cielab[2]} ]"

    def __repr__(self) -> str:
        return self.__str__()