import json
from genetic_algorithm.artist_palette import ArtistPalette
from lib.input_handler import InputHandler

with open('config.json', 'r') as f:
    input = json.load(f)
    input_handler = InputHandler(input)

artist_palette = ArtistPalette(input_handler.lab_color_palette, input_handler.population_n)
#for i in range(2):
artist_palette.mix_new_generation(input_handler)

'''
print(f"The target is {input_handler.target_color}\n")
for color in artist_palette.get_best_colors(input_handler.target_color):
    delta_e = color.get_delta(input_handler.target_color)
    print(f"The delta_e is {delta_e}\n")
'''