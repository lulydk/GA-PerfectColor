import sys
import json
import numpy as np
from utils.constants import *
from utils.window_frame import frame1, grid
from utils.input_handler import InputHandler
import PyQt5.QtGui as qtg
from PyQt5.QtWidgets import QApplication, QWidget
from colormath.color_conversions import convert_color
from colormath.color_objects import LabColor, sRGBColor
from genetic_algorithm.artist_palette import ArtistPalette


def cut(iteration, delta, best_ever, cut_method, cut_generation, cut_delta):
    if (cut_method == GENERATIONS):
        return iteration >= cut_generation
    elif (cut_method == TRESHOLD):
        return delta <= cut_delta
    else:
        if (iteration - best_ever[0] > cut_generation and abs(delta - best_ever[1]) < ERROR):
            print("Cut by exhaustion")
            return True

def run_simulation(target, input_handler):
    artist_palette = ArtistPalette(input_handler.color_palette, input_handler.population_n, target)
    all_best = []
    all_best.append(artist_palette.best_color)
    delta_e = all_best[0].get_delta(target)
    all_colors = []
    all_colors.append(artist_palette.color_palette)
    iteration_count = 0
    best_ever = np.zeros(2)
    best_ever[0], best_ever[1] = iteration_count, delta_e
    while (not cut(iteration_count,delta_e,best_ever,input_handler.cut_method,input_handler.cut_generation,input_handler.cut_delta)):
        artist_palette.mix_new_generation(input_handler)
        all_colors.append(artist_palette.color_palette)
        curr_best = artist_palette.best_color
        delta_e = curr_best.get_delta(target)
        all_best.append(curr_best)
        if (abs(delta_e - best_ever[1]) >= ERROR):
            best_ever[0] = iteration_count
            best_ever[1] = delta_e
        print(f"#{iteration_count} with delta_e = {delta_e}")
        iteration_count += 1
    return all_colors, all_best, iteration_count

def run_visualization(target, finished_color, input_handler):
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

def write_recipe(is_rgb, target, best):
    coords = "RGB"
    if (not is_rgb):
        coords = "L*a*b*"
    with open("output/recipe.txt", "w") as external_file:
        add_text = f"DELTA\t\t\t{round(best.get_delta(target),4)}\n\nTARGET COLOR\t{coords}: {target.coord}\n\nBEST COLOR\t\t{coords}: {best.coord}\n\nRECIPE\n[ Base color ]: Proportion\n\n{best}"
        print(add_text, file=external_file)
    print("Results in output/recipe.txt")

def write_output_data(all_best_colors, target, population_size):
    with open("output/graphics.txt", "w") as external_file:
        print(population_size, file=external_file)
        for generation in all_best_colors:
            generation_string = ' '.join([f'{color.get_fitness(target)}' for color in generation])
            print(generation_string, file=external_file)
    print("Simulation data in output/graphics.txt")

def main():
    with open('config.json', 'r') as f:
        input = json.load(f)
        input_handler = InputHandler(input)
    # Simulation
    target = input_handler.target_color
    all_colors, all_best_colors, total_iterations = run_simulation(target, input_handler)
    finished_color = all_best_colors[total_iterations]
    # File outputs
    ## Recipe with color proportions
    write_recipe(input_handler.work_with_rgb, target, finished_color)
    ## Data for graphics
    write_output_data(all_colors, target, input_handler.population_n)
    # Visualization
    run_visualization(target, finished_color, input_handler)

if __name__ == "__main__":
    main()