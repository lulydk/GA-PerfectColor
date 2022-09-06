import numpy as np
from random import randint
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from genetic_algorithm.color import Color

class InputHandler:

    def random_color_palette(self, filepath):
        color_count = randint(3,100)
        arr = np.random.randint(0, 255, (color_count,3))
        with open(filepath, "w") as file:
            for color in arr:
                file.write(f"{color[0]} {color[1]} {color[2]}\n")
        return arr

    def arr_to_colors(self, color_array, work_with_rgb):
        color_palette = []
        if (work_with_rgb):
            for color in color_array:
                color_palette.append(Color(color[0], color[1], color[2], True))
        else:
            for color in color_array:
                color_lab = convert_color(sRGBColor(color[0]/255,color[1]/255,color[2]/255, False), LabColor)
                new_color = Color(color_lab.lab_l, color_lab.lab_a, color_lab.lab_b, False)
                color_palette.append(new_color)
        return color_palette
    
    def __init__(self, input):
        self.work_with_rgb = input['work_with_rgb']
        # Color Palette
        self.input_color_palette = []
        if (input['random_palette']):
            self.input_color_palette = self.random_color_palette(input['color_palette_file'])
        else:
            self.input_color_palette = np.genfromtxt(input['color_palette_file'])
            if (len(self.input_color_palette) == 0):
                raise Exception(f"Empty input file {input['color_palette_file']}")
        self.color_palette = self.arr_to_colors(self.input_color_palette, input['work_with_rgb'])
        # Target Color
        self.rgb_target = input['target_color']
        if (input['work_with_rgb']):
            self.target_color = Color(input['target_color'][0], input['target_color'][1], input['target_color'][2], True)
        else:
            target_color_lab = convert_color(sRGBColor(input['target_color'][0]/255,input['target_color'][1]/255,input['target_color'][2]/255, False), LabColor)
            self.target_color = Color(target_color_lab.lab_l, target_color_lab.lab_a, target_color_lab.lab_b, False)
        # GA Hyperparameters
        ## Implementation
        self.implementation = input['hyperparameters']['implementation']
        ## Selection
        self.selection_method = input['hyperparameters']['selection']
        self.population_n = input['hyperparameters']['population_n']
        self.individuals_k = input['hyperparameters']['individuals_k']
        self.individuals_m = input['hyperparameters']['individuals_m']
        ## Crossover
        self.cross_prob = input['hyperparameters']['cross_prob']
        ## Mutation
        self.mut_prob = input['hyperparameters']['mutation_prob']
        ## Cutting Method
        self.cut_method = input['hyperparameters']['cut_criteria']['method']
        self.cut_generation = input['hyperparameters']['cut_criteria']['max_num_generations']
        self.cut_delta = input['hyperparameters']['cut_criteria']['delta_treshold']