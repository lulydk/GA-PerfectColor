import numpy as np
from random import randint
from genetic_algorithm.color import Color

class ArtistPalette:

    # base_colors = [ color1, ..., colorG ] GENOMES
    # color_palette = [ color1, ..., colorN ] CURRENT GENERATION

    def get_best_colors(self, target_color):
        return sorted(self.color_palette, key=lambda c: c.get_delta(target_color))

    def mix_new_generation():
        pass

    # color_proportions = { color1: 0.25, color2: 0.40, color3: 0.35 }
    def generate_color(self):
        sum = 0
        color_proportions = {}
        # Generates a random number for each proportion
        for color in self.base_colors:
            proportion = randint(0,100)
            sum += proportion
            color_proportions[color] = proportion
        # The sum of proportions has to be equal to 1
        for color in color_proportions:
            color_proportions[color] /= sum
        # Create new color based on those proportions
        cielab = np.zeros(3)
        for key in color_proportions:
            cielab[0] += (key.cielab[0] * color_proportions[key])
            cielab[1] += (key.cielab[1] * color_proportions[key])
            cielab[2] += (key.cielab[2] * color_proportions[key])
        return Color(cielab[0],cielab[1],cielab[2], color_proportions)

    def spawn_colors(self, population_count):
        color_palette = []
        for i in range(population_count):
            color_palette.append(self.generate_color())
        return color_palette

    def __init__(self, base_colors, population_count):
        self.base_colors = base_colors
        self.color_palette = self.spawn_colors(population_count)