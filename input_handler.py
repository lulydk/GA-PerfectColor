class InputHandler:
    
    def __init__(self, data):
        
        self.implementation = data['implementation']
        
        self.selection = data['selection']
        self.population_n = data['population_n']
        self.individuals_k = data['individuals_k']
        self.individuals_m = data['individuals_m']
        self.treshold = data['treshold']

        self.crossover = data['crossover']
        self.coss_prob = data['coss_prob']

        self.mutation = data['mutation']
        self.mut_prob = data['mut_prob']

        self.cut_method = data['cut_criteria']['method']
        self.cut_value = data['cut_criteria']['value']