import json
from lib.input_handler import InputHandler
from colormath.color_conversions import convert_color
from colormath.color_objects import LabColor, sRGBColor
from genetic_algorithm.artist_palette import ArtistPalette

with open('config.json', 'r') as f:
    input = json.load(f)
    input_handler = InputHandler(input)

artist_palette = ArtistPalette(input_handler.lab_color_palette, input_handler.population_n)
for i in range(200):
    artist_palette.mix_new_generation(input_handler)
best = artist_palette.get_best_colors(input_handler.target_color)[0]

target_color = convert_color(LabColor(input_handler.target_color.cielab[0], input_handler.target_color.cielab[1], input_handler.target_color.cielab[2]), sRGBColor)
color1 = sRGBColor(target_color.clamped_rgb_r, target_color.clamped_rgb_g, target_color.clamped_rgb_b)

best_color = convert_color(LabColor(best.cielab[0], best.cielab[1], best.cielab[2]), sRGBColor)
color2 = sRGBColor(best_color.clamped_rgb_r, best_color.clamped_rgb_g, best_color.clamped_rgb_b)

with open("output.txt", "w") as external_file:
    add_text = f"TARGET COLOR\nL*a*b*: {input_handler.target_color}\n\nBEST COLOR\nL*a*b*: {best.cielab}\nColor proportions:\n{best}\n\nDelta: {round(best.get_delta(input_handler.target_color),4)}"
    print(add_text, file=external_file)
    external_file.close()

print("Results in output.txt")

#'''
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from functions import frame1, grid

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Perfect Color")
window.setFixedWidth(800)

frame1(color1.get_rgb_hex(), color2.get_rgb_hex(),f"L*a*b*: {input_handler.target_color}",f"L*a*b*: {best.cielab}\n\nColor proportions:\n{best}\n\nDelta: {round(best.get_delta(input_handler.target_color),4)}")
window.setLayout(grid)

window.show()
sys.exit(app.exec())
#'''