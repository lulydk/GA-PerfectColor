import math, random

# Gets the best colors based on their closeness to the target color
# The more fit, the more times it appears in the final list of lenght k
def elite(generation, k_value, target_color):
    elite_colors = []
    # From smaller to larger distances
    sorted_colors = sorted(generation, key=lambda c: c.get_delta(target_color))
    i = 0
    for color in sorted_colors:
        elite_len = len(elite_colors)
        # If I didn't surpass the expected lenght,
        # keep filling the elite list with the best
        if(elite_len < k_value):
            n_i = math.ceil((k_value - i)/len(generation))
            # If the amount of times I should include it
            # surpasses the desired lenght, fix it
            if(n_i > k_value-elite_len):
                n_i = k_value-elite_len
            for j in range(n_i):
                elite_colors.append(color)
            i += 1
        else:
            break
    return elite_colors

# The better the fitness, the greater the chances to be selected
# However, the less fit still get a chance to be chosen
def roulette(generation, k_value, target_color):
    # Sum the fitness of every color
    fitness = list(map(lambda c: c.get_delta(target_color), generation))
    fit_sum = sum(fitness)
    # Transform it to proportions:
    # The shortest the distance, the higher the value
    fitness = list(map(lambda f: fit_sum/f, fitness))
    prop_sum = sum(fitness)
    # Normalize between 0 and 1
    fitness = list(map(lambda p: p/prop_sum, fitness))
    # Cumulative proportions
    cumulative_sum = 0
    cumulative_props = []
    for prop in fitness:
        cumulative_sum += prop
        cumulative_props.append(cumulative_sum)
    # Generate k random numbers
    # and select the k colors that verify
    selected_colors = []
    for i in k_value:
        selected_value = random.random()
        j = 0
        for value in cumulative_props:
            if(value >= selected_value):
                selected_colors.append(generation[j])
            j += 1
    return selected_colors

# Get two random colors from the generation
# and the one with the best fitness wins
# Repeat until k colors are selected
def det_tournament(generation, k_value, target_color):
    winner_colors = []
    for i in range(k_value):
        idx1 = random.randint(0,len(generation)-1)
        color1 = generation[idx1]
        idx2 = random.randint(0,len(generation)-1)
        while(idx1 == idx2):
            idx2 = random.randint(0,len(generation)-1)
        color2 = generation[random.randint(0,len(generation)-1)]
        if(color1.get_delta(target_color) < color1.get_delta(target_color)):
            winner_colors.append(color1)
        else:
            winner_colors.append(color2)
    return winner_colors