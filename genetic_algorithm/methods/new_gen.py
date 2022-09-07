from math import floor, ceil
from genetic_algorithm.methods.selection import selection

def fill_all(current_generation, children, selection_proportion, target_color):
    current_best = sorted(current_generation, key=lambda c: c.get_fitness(target_color), reverse=True)[0]
    population_size = len(current_generation)
    group1 = floor(selection_proportion*(population_size-1))
    group2 = ceil((1-selection_proportion)*(population_size-1))
    from_children = selection("elite", generation=children, k_value=group1, target_color=target_color, m_value=None)
    from_current = selection("elite", generation=current_generation, k_value=group2, target_color=target_color, m_value=None)
    return [current_best] + from_children + from_current

def fill_parent(current_generation, children, k_value, target_color):
    population_size = len(current_generation)
    if (k_value == population_size):
        return children
    elif (k_value > population_size):
        selected_children = selection(None, children, population_size, target_color, None)
        return selected_children
    else:
        selected = selection(None, current_generation, population_size-len(children), target_color, None)
        return children + selected