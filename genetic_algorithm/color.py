import numpy as np
from lib.color_diff import *
from colormath.color_conversions import convert_color
from colormath.color_objects import sRGBColor, LabColor

class Color:

    # coord = [L, a, b] or [R, G, B]
    # color_proportions = { color1: 0.25, color2: 0.40, color3: 0.35 }
    
    def get_delta(self, other):
        if (self.is_rgb and other.is_rgb):
            delta_e = delta_e_rgb(self.coord, other.coord)
        else:
            if (not self.is_rgb and not other.is_rgb):
                color_lab = LabColor(self.coord[0], self.coord[1], self.coord[2])
                other_lab = LabColor(other.coord[0], other.coord[1], other.coord[2])
            elif (self.is_rgb and not other.is_rgb):
                color_lab = convert_color(sRGBColor(self.coord[0],self.coord[1],self.coord[2], True), LabColor)
                other_lab = LabColor(other.coord[0], other.coord[1], other.coord[2])
            else:
                color_lab = LabColor(self.coord[0], self.coord[1], self.coord[2])
                other_lab = convert_color(sRGBColor(other.coord[0],other.coord[1],other.coord[2], True), LabColor)
            delta_e = delta_e_cie2000(color_lab, other_lab)
        return delta_e

    def __init__(self, coord0, coord1, coord2, rgb, color_proportions=None):
        self.is_rgb = rgb
        self.coord = np.zeros(3)
        self.coord[0] = coord0
        self.coord[1] = coord1
        self.coord[2] = coord2
        self.color_proportions = color_proportions

    def __hash__(self) -> int:
        return hash((self.coord[0], self.coord[1], self.coord[2]))

    def __eq__(self, other: object) -> bool:
        return self.get_delta(other) == 0

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        if(self.color_proportions == None):
            return str(self.coord)
        return '\n'.join([f'{key}: {round(value,4)}' for key, value in self.color_proportions.items()])

    def __repr__(self) -> str:
        return self.__str__()