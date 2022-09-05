import sys
import json
import numpy as np
from lib.constants import *
from functions import frame1, grid
from lib.input_handler import InputHandler
from PyQt5.QtWidgets import QApplication, QWidget
from colormath.color_conversions import convert_color
from colormath.color_objects import LabColor, sRGBColor
from genetic_algorithm.artist_palette import ArtistPalette


with open('config.json', 'r') as f:
    input = json.load(f)
    input_handler = InputHandler(input)

def cut(iteration, delta, best=None):
    if (input_handler.cut_method == GENERATIONS):
        return iteration >= input_handler.cut_value
    elif (input_handler.cut_method == TRESHOLD):
        return delta <= input_handler.cut_value
    else:
        if (iteration - best[0] > 200 and abs(delta - best[1]) < 0.00001):
            print("Cut by exhaustion")
            return True

def main():
    #'''
    # Simulation
    artist_palette = ArtistPalette(input_handler.color_palette, input_handler.population_n, input_handler.target_color)
    target = input_handler.target_color
    delta_e = 1000
    iteration_count = 0
    best_result = np.zeros(2)
    best_result[0] = iteration_count
    best_result[1] = delta_e
    while (not cut(iteration_count,delta_e,best_result)):
        artist_palette.mix_new_generation(input_handler)
        best = artist_palette.best_color
        delta_e = best.get_delta(target)
        if (abs(delta_e - best_result[1]) >= 0.00001):
            best_result[0] = iteration_count
            best_result[1] = delta_e
        print(f"#{iteration_count} with delta_e = {delta_e}")
        iteration_count += 1
    if (input_handler.work_with_rgb):
        coords = "RGB"
    else:
        target_color = convert_color(LabColor(target.coord[0], target.coord[1], target.coord[2]), sRGBColor)
        color1 = sRGBColor(target_color.clamped_rgb_r, target_color.clamped_rgb_g, target_color.clamped_rgb_b)
        best_color = convert_color(LabColor(best.coord[0], best.coord[1], best.coord[2]), sRGBColor)
        color2 = sRGBColor(best_color.clamped_rgb_r, best_color.clamped_rgb_g, best_color.clamped_rgb_b)
        coords = "L*a*b"
    # File output
    with open("output.txt", "w") as external_file:
        add_text = f"TARGET COLOR\n{coords}: {target}\n\nBEST COLOR\n{coords}: {best.coord}\nColor proportions:\n{best}\n\nDelta: {round(best.get_delta(target),4)}"
        print(add_text, file=external_file)
        external_file.close()
    print("Results in output.txt")
    # Visualization
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Perfect Color")
    window.setFixedWidth(800)
    if (input_handler.work_with_rgb):
        frame1(f"rgb({int(target.coord[0])},{int(target.coord[1])},{int(target.coord[2])})", f"rgb({int(best.coord[0])},{int(best.coord[1])},{int(best.coord[2])})",f"RGB: {target}",f"RGB: [{int(best.coord[0])} {int(best.coord[1])} {int(best.coord[2])}]\n\nColor proportions:\n{best}\n\nDelta: {round(best.get_delta(target),4)}")
    else:
        frame1(color1.get_rgb_hex(), color2.get_rgb_hex(),f"{coords}: {target}",f"{coords}: {best.coord}\n\nColor proportions:\n{best}\n\nDelta: {round(best.get_delta(target),4)}")
    window.setLayout(grid)
    window.show()
    sys.exit(app.exec())
    #'''

if __name__ == "__main__":
    main()