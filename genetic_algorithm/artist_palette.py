import numpy as np
from random import *
from utils.constants import *
from genetic_algorithm.color import Color
from genetic_algorithm.methods.selection import *
from genetic_algorithm.methods.crossover import *
from genetic_algorithm.methods.new_gen import *

class ArtistPalette:

    # base_colors = [ color1, ..., colorG ] GENOMES
    # color_palette = [ color1, ..., colorN ] CURRENT GENERATION

    def get_best_colors(self) -> Color:
        return sorted(self.color_palette, key=lambda c: c.get_fitness(self.target_color), reverse=True)


    def mix_new_generation(self, input_data) -> None:

        # Selection
        selected = selection(input_data.selection_method, self.color_palette, input_data.individuals_k, self.target_color, input_data.individuals_m)

        # Crossover
        children = one_point_crossover(selected, input_data.cross_prob, self.base_colors)
        
        # Mutation
        mutated_children = []
        for c in children:
            if (random.uniform(0,1) < input_data.mut_prob):
                new = self.generate_color()
                mutated_children.append(new)
            else:
                mutated_children.append(c)
               
        # Forming new generation
        new_generation = []
        if (input_data.implementation == FILL_ALL):
            new_generation = fill_all(self.color_palette, mutated_children, input_data.selection_proportion, input_data.target_color)
        elif (input_data.implementation == FILL_PARENT):
            new_generation = fill_parent(self.color_palette, mutated_children, input_data.individuals_k, input_data.target_color)
        
        self.color_palette = new_generation
        self.best_color = self.get_best_colors()[0]


    # color_proportions = { color1: 0.25, color2: 0.40, color3: 0.35 }
    def generate_color(self) -> Color:
        sum = 0
        color_proportions = {}
        # Generates a random number for each proportion
        for color in self.base_colors:
            proportion = random.uniform(0,1)
            sum += proportion
            color_proportions[color] = proportion
        # The sum of proportions has to be equal to 1
        for color in color_proportions:
            color_proportions[color] /= sum
        # Create new color based on those proportions
        coord = np.zeros(3)
        for key in color_proportions:
            coord[0] += (key.coord[0] * color_proportions[key])
            coord[1] += (key.coord[1] * color_proportions[key])
            coord[2] += (key.coord[2] * color_proportions[key])
        return Color(coord[0],coord[1],coord[2], self.base_colors[0].is_rgb, color_proportions, self.target_color)

    def spawn_colors(self, population_count) -> list:
        color_palette = []
        for i in range(population_count):
            color_palette.append(self.generate_color())
        return color_palette

    def __init__(self, base_colors, population_count, target_color):
        self.base_colors = base_colors
        self.target_color = target_color
        self.color_palette = self.spawn_colors(population_count)
        self.best_color = self.get_best_colors()[0]