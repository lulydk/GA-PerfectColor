from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from genetic_algorithm.color import Color

class InputHandler:

    def arr_to_colors(self, color_array, work_with_rgb):
        color_palette = []
        if (work_with_rgb):
            for color in color_array:
                color_palette.append(Color(color[0], color[1], color[2], True))
        else:
            for color in color_array:
                color_lab = convert_color(sRGBColor(color[0],color[1],color[2], True), LabColor)
                color_palette.append(Color(color_lab.lab_l, color_lab.lab_a, color_lab.lab_b, False))
        return color_palette
    
    def __init__(self, input):
        self.work_with_rgb = input['work_with_rgb']
        self.color_palette = self.arr_to_colors(input['color_palette'], input['work_with_rgb'])
        if(input['work_with_rgb']):
            self.target_color = Color(input['target_color'][0], input['target_color'][1], input['target_color'][2], True)
        else:
            target_color_lab = convert_color(sRGBColor(input['target_color'][0],input['target_color'][1],input['target_color'][2], True), LabColor)
            self.target_color = Color(target_color_lab.lab_l, target_color_lab.lab_a, target_color_lab.lab_b, False)
        # GA Hyperparameters
        ## Implementation
        self.implementation = input['hyperparameters']['implementation']
        ## Selection
        self.selection_method = input['hyperparameters']['selection']
        self.population_n = input['hyperparameters']['population_n']
        self.individuals_k = input['hyperparameters']['individuals_k']
        self.individuals_m = input['hyperparameters']['individuals_m']
        self.treshold = input['hyperparameters']['treshold']
        ## Crossover
        self.crossover_method = input['hyperparameters']['crossover']
        self.cross_prob = input['hyperparameters']['cross_prob']
        ## Mutation
        self.mutation_method = input['hyperparameters']['mutation']
        self.mut_prob = input['hyperparameters']['mut_prob']
        ## Cutting Method
        self.cut_method = input['hyperparameters']['cut_criteria']['method']
        self.cut_value = input['hyperparameters']['cut_criteria']['value']