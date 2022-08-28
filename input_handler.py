from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color

class InputHandler:

    def arr_to_lab(self, color_array):
        lab_color_palette = []
        for color in color_array:
            color_rgb = sRGBColor(color[0],color[1],color[2])
            lab_color_palette.append(convert_color(color_rgb, LabColor))
            # lab_color_palette.append(color_rgb)
        return lab_color_palette
    
    def __init__(self, input):

        self.lab_color_palette = self.arr_to_lab(input['color_palette'])
        # self.goal_color = sRGBColor(input['goal_color'][0],input['goal_color'][1],input['goal_color'][2])
        self.goal_color = convert_color(sRGBColor(input['goal_color'][0],input['goal_color'][1],input['goal_color'][2]), LabColor)
        
        # GA Hyperparameters
        ## Implementation
        self.implementation = input['hyperparameters']['implementation']
        ## Selection
        self.selection = input['hyperparameters']['selection']
        self.population_n = input['hyperparameters']['population_n']
        self.individuals_k = input['hyperparameters']['individuals_k']
        self.individuals_m = input['hyperparameters']['individuals_m']
        self.treshold = input['hyperparameters']['treshold']
        ## Crossover
        self.crossover = input['hyperparameters']['crossover']
        self.cross_prob = input['hyperparameters']['cross_prob']
        ## Mutation
        self.mutation = input['hyperparameters']['mutation']
        self.mut_prob = input['hyperparameters']['mut_prob']
        ## Cutting Method
        self.cut_method = input['hyperparameters']['cut_criteria']['method']
        self.cut_value = input['hyperparameters']['cut_criteria']['value']