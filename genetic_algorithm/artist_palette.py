import numpy as np
from random import *
from lib.constants import *
from genetic_algorithm.color import Color
from genetic_algorithm.methods.selection import *
from genetic_algorithm.methods.crossover import *

class ArtistPalette:

    # base_colors = [ color1, ..., colorG ] GENOMES
    # color_palette = [ color1, ..., colorN ] CURRENT GENERATION

    def get_best_colors(self, target_color):
        return sorted(self.color_palette, key=lambda c: c.get_delta(target_color))

    def mix_new_generation(self, input_data):
        # Selection
        selected = []
        if (input_data.selection_method == ELITE):
            selected = elite(self.color_palette, input_data.individuals_k, input_data.target_color)
        elif (input_data.selection_method == ROULETTE):
            selected = roulette(self.color_palette, input_data.individuals_k, input_data.target_color)
        elif (input_data.selection_method == DET_TOURNAMENT):
            selected = det_tournament(self.color_palette, input_data.individuals_k, input_data.target_color)
        '''
        print(f"selected has #{len(selected)} colors")
        print("Parents:\n")
        for s in selected:
            print(f"{s}\n")
        '''
        # Crossover
        children = []
        if (input_data.crossover_method == ONE_POINT):
            children = one_point_crossover(selected, self.base_colors)
        elif (input_data.crossover_method == TWO_POINT):
            pass
        '''
        print("Children:\n")
        for c in children:
            print(f"{c}\n")
        '''
        # Mutation
        '''
        mutated_children = children
        print("Mutations:\n")
        for m in mutated_children:
            print(f"{c}\n")
        print(f"get new gen from #{len(children)} children")
        '''
        new_generation = []
        # Forming new generation
        if (input_data.implementation == FILL_ALL):
            pass
        elif (input_data.implementation == FILL_PARENT):
            if (input_data.individuals_k > input_data.population_n):
                new_generation = children[:input_data.population_n]
            else:
                new_generation = children
                best_last_gen = self.get_best_colors(input_data.target_color)
                for i in range(input_data.population_n - input_data.individuals_k):
                    new_generation.append(best_last_gen[i])
        '''
        print("New Gen:\n")
        for n in new_generation:
            print(f"{n}\n")
        '''
        self.color_palette = new_generation

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
        self.iter = 0