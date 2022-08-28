import json
from color_diff import delta_e_cie2000
from input_handler import InputHandler

with open('config.json', 'r') as f:
    input = json.load(f)
    input_handler = InputHandler(input)

for color in input_handler.lab_color_palette:
    delta_e = delta_e_cie2000(color, input_handler.goal_color)
    print(f"The delta_e between {color} and {input_handler.goal_color} is {delta_e}")