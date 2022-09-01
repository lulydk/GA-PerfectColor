import numpy as np
from math import floor
from random import random, randint
from genetic_algorithm.color import Color

# Ramdomly-based grouping:
# Takes the first half and the reversed second half,
# or takes all odd indexes in one group and all evens in another
def divide_population(population):
    group1 = []
    group2 = []
    middle = floor(len(population)/2)
    # Throw a coin
    if (random() > 0.5):
        group1 = population[0:middle]
        group2 = population[:middle-1:-1]
    else:
        group1 = population[0::2]
        group2 = population[1::2]
    return group1, group2

# Randomly chooses a locus,
# then swaps alleles from that point onwards
def one_point_crossover(population, genes):
    children = []
    pop_len = len(population)
    if (pop_len%2 != 0):
        population.append(population[pop_len-1])
        pop_len += 1
    parents1, parents2 = divide_population(population)
    for p1,p2 in zip(parents1,parents2):
        # If the genes are few, the children have
        # increased chances to be copies of their parents
        locus = randint(0,len(genes))
        color_prop1 = {}
        color_prop2 = {}
        for idx in range(len(genes)):
            if(idx < locus):
                color_prop1[genes[idx]] = p1.color_proportions[genes[idx]]
                color_prop2[genes[idx]] = p2.color_proportions[genes[idx]]
            else:
                color_prop1[genes[idx]] = p2.color_proportions[genes[idx]]
                color_prop2[genes[idx]] = p1.color_proportions[genes[idx]]
        sum_prop1 = sum(color_prop1.values())
        sum_prop2 = sum(color_prop2.values())
        for color in genes:
            color_prop1[color] /= sum_prop1
            color_prop2[color] /= sum_prop2
        cielab1 = np.zeros(3)
        cielab2 = np.zeros(3)
        for key in genes:
            cielab1[0] += (key.cielab[0] * color_prop1[key])
            cielab1[1] += (key.cielab[1] * color_prop1[key])
            cielab1[2] += (key.cielab[2] * color_prop1[key])
            cielab2[0] += (key.cielab[0] * color_prop2[key])
            cielab2[1] += (key.cielab[1] * color_prop2[key])
            cielab2[2] += (key.cielab[2] * color_prop2[key])
        children.append(Color(cielab1[0],cielab1[1],cielab1[2], color_prop1))
        children.append(Color(cielab2[0],cielab2[1],cielab2[2], color_prop2))
    return children