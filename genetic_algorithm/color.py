import numpy as np
from lib.color_diff import *
from colormath.color_conversions import convert_color
from colormath.color_objects import sRGBColor, LabColor

class Color:

    # coord = [L, a, b] or [R, G, B]
    # color_proportions = { color1: 0.25, color2: 0.40, color3: 0.35 }

    epsilon = 0.0000001 # Avoid dividing by zero when getting fitness
    
    def to_rgb_string(self):
        if (self.is_rgb):
            return f"[ {int(self.coord[0])}, {int(self.coord[1])}, {int(self.coord[2])} ]"
        else:
            conversion = convert_color(LabColor(self.coord[0], self.coord[1], self.coord[2]), sRGBColor)
            rgb_color = [conversion.clamped_rgb_r, conversion.clamped_rgb_g, conversion.clamped_rgb_b]
            return f"[ {int(rgb_color[0]*255)}, {int(rgb_color[1]*255)}, {int(rgb_color[2]*255)} ]"

    def get_delta(self, other):
        if (self.is_rgb and other.is_rgb):
            delta_e = delta_e_rgb(self.coord, other.coord)
        else:
            delta_e = delta_e_lab(self.coord, other.coord)
            '''
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
            '''
        return delta_e

    def set_fitness(self, target_color):
        if (target_color == None):
            return 0
        return 1/(self.get_delta(target_color) + Color.epsilon)

    def get_fitness(self, target_color):
        if (self.fitness == 0):
            self.set_fitness(target_color)
        return self.fitness

    def __init__(self, coord0, coord1, coord2, rgb, color_proportions=None, target_color=None):
        self.is_rgb = rgb
        self.coord = np.zeros(3)
        self.coord[0] = coord0
        self.coord[1] = coord1
        self.coord[2] = coord2
        self.color_proportions = color_proportions
        self.fitness = self.set_fitness(target_color)

    def __hash__(self) -> int:
        return hash((self.coord[0], self.coord[1], self.coord[2]))

    def __eq__(self, other: object) -> bool:
        if (other == None):
            return False
        return self.coord == other.coord

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


    def __str__(self) -> str:
        if(self.color_proportions == None):
            return str(self.coord)
        return '\n'.join([f'{key.to_rgb_string()}: {round(value,4)}' for key, value in self.color_proportions.items()])

    def __repr__(self) -> str:
        return self.__str__()