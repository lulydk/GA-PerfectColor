import numpy as np
from random import *
from lib.constants import *
from genetic_algorithm.color import Color
from genetic_algorithm.methods.mutation import *
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
        
        # Crossover
        children = []
        if (input_data.crossover_method == ONE_POINT):
            children = one_point_crossover(selected, self.base_colors)
        elif (input_data.crossover_method == TWO_POINT):
            pass
        
        # Mutation
        mutated_children = []
        #mutated_children = children
        if (input_data.mutation_method == GEN):
            #mutated_children = gen_mutation(children,self.base_colors,input_data.mut_prob)
            pass
        else:
            for c in children:
                if (random() > 0.03):
                    mutated_children.append(self.generate_color())
                else:
                    mutated_children.append(c)
                    
        # Forming new generation
        new_generation = []
        if (input_data.implementation == FILL_ALL):
            all = mutated_children + self.color_palette
            new_generation = sorted(all, key=lambda c: c.get_delta(input_data.target_color))[:input_data.population_n]
        elif (input_data.implementation == FILL_PARENT):
            if (input_data.individuals_k > input_data.population_n):
                new_generation = mutated_children[:input_data.population_n]
            else:
                new_generation = mutated_children
                best_last_gen = self.get_best_colors(input_data.target_color)
                for i in range(input_data.population_n - input_data.individuals_k):
                    new_generation.append(best_last_gen[i])
        
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
        coord = np.zeros(3)
        for key in color_proportions:
            coord[0] += (key.coord[0] * color_proportions[key])
            coord[1] += (key.coord[1] * color_proportions[key])
            coord[2] += (key.coord[2] * color_proportions[key])
        return Color(coord[0],coord[1],coord[2], self.base_colors[0].is_rgb, color_proportions)

    def spawn_colors(self, population_count):
        color_palette = []
        for i in range(population_count):
            color_palette.append(self.generate_color())
        return color_palette

    def __init__(self, base_colors, population_count):
        self.base_colors = base_colors
        self.color_palette = self.spawn_colors(population_count)