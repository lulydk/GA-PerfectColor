import sys
import json
import numpy as np
from lib.constants import *
from lib.window_frame import frame1, grid
from lib.input_handler import InputHandler
import PyQt5.QtGui as qtg
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
        if (iteration - best[0] > 200 and abs(delta - best[1]) < ERROR):
            print("Cut by exhaustion")
            return True

def run_simulation(target, color_palette, population_n):
    artist_palette = ArtistPalette(color_palette, population_n, target)
    best = artist_palette.best_color
    delta_e = best.get_fitness(target)
    iteration_count = 0
    best_ever = np.zeros(2)
    best_ever[0], best_ever[1] = iteration_count, delta_e
    while (not cut(iteration_count,delta_e,best_ever)):
        artist_palette.mix_new_generation(input_handler)
        best = artist_palette.best_color
        delta_e = best.get_delta(target)
        if (abs(delta_e - best_ever[1]) >= ERROR):
            best_ever[0] = iteration_count
            best_ever[1] = delta_e
        if (iteration_count % 10 == 0):
            print(f"#{iteration_count} with delta_e = {delta_e}")
        iteration_count += 1
    return best

def write_recipe(is_rgb, target, best):
    coords = "RGB"
    if (not is_rgb):
        coords = "L*a*b*"
    with open("output/recipe.txt", "w") as external_file:
        add_text = f"DELTA\t\t\t{round(best.get_delta(target),4)}\n\nTARGET COLOR\t{coords}: {target.coord}\n\nBEST COLOR\t\t{coords}: {best.coord}\n\nRECIPE\n[ Base color ]: Proportion\n\n{best}"
        print(add_text, file=external_file)
    print("Results in output/recipe.txt")

def run_visualization(target, finished_color):
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Perfect Color")
    window.setWindowIcon(qtg.QIcon('icon.png'))
    window.setFixedWidth(800)
    if (input_handler.work_with_rgb):
        frame1( 
                f"rgb({int(target.coord[0])},{int(target.coord[1])},{int(target.coord[2])})",
                f"RGB: {input_handler.rgb_target}",
                f"rgb({int(finished_color.coord[0])},{int(finished_color.coord[1])},{int(finished_color.coord[2])})",
                f"RGB: [{int(finished_color.coord[0])}, {int(finished_color.coord[1])}, {int(finished_color.coord[2])}]",
                f"Delta: {round(finished_color.get_delta(target),4)}",
                f"Color proportions:\n{finished_color}"
              )
    else:
        best_to_rgb = convert_color(LabColor(finished_color.coord[0], finished_color.coord[1], finished_color.coord[2]), sRGBColor)
        target_to_rgb = sRGBColor(input_handler.rgb_target[0]/255, input_handler.rgb_target[1]/255, input_handler.rgb_target[2]/255, False)
        frame1(
                target_to_rgb.get_rgb_hex(),
                f"- L*a*b: [ {int(target.coord[0])}, {int(target.coord[1])}, {int(target.coord[2])} ]\n- RGB: {input_handler.rgb_target}",
                best_to_rgb.get_rgb_hex(),
                f"- L*a*b: [ {int(finished_color.coord[0])}, {int(finished_color.coord[1])}, {int(finished_color.coord[2])} ]\n- RGB: {finished_color.to_rgb_string()}",
                f"Delta: {round(finished_color.get_delta(target),4)}",
                f"Color proportions:\n{finished_color}"
              )
    window.setLayout(grid)
    window.show()
    sys.exit(app.exec())

def main():
    # Simulation
    target = input_handler.target_color
    finished_color = run_simulation(target, input_handler.color_palette, input_handler.population_n)
    # File outputs
    ## Recipe with color proportions
    write_recipe(input_handler.work_with_rgb, target, finished_color)
    ## Data for graphics
    with open("output/graphics.txt", "w") as external_file:
        add_text = f""
        print(add_text, file=external_file)
    print("Simulation data in output/graphics.txt")
    # Visualization
    run_visualization(target, finished_color)

if __name__ == "__main__":
    main()