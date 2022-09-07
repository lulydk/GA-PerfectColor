import json
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)

def get_values(filename="graphics.txt"):
    path = f"C:/Users/lulyd/Documents/GA-PerfectColor/output/{filename}"
    with open(path, "r") as file:
        population_size = int(file.readline())
        content = file.read()
    array = list(map(float, content.split()))
    return population_size, array

def get_benchmark_values(runs):
    population_n, array1 = get_values(f"graphics1.txt")
    sum_runs = array1
    for i in range(runs - 1):
        population_n, array = get_values(f"graphics{i+2}.txt")
        for i in range(population_n):
            sum_runs[i] = (sum_runs[i]+array[i])/2
    return population_n, sum_runs
    
def get_fitness_vs_all_colors(run_benchmark, benchmark_runs=0):
    if (run_benchmark):
        population_size, array = get_benchmark_values(benchmark_runs)
    else:
        population_size, array = get_values()
    fig, ax = plt.subplots()
    ax.set_title('Fitness through the generations')
    ax.set_ylabel('Fitness')
    ax.set_xlabel('Colors through generations')
    #ax.xaxis.set_minor_locator(MultipleLocator(population_size))
    #x = list(map(lambda num: num/population_size,range(len(array))))
    #ax.set_xlabel('Generations')
    #ax.xaxis.set_minor_locator(MultipleLocator(1))
    #ax.plot(x, array)
    ax.plot(array)
    plt.show()

if __name__ == "__main__":
    with open('config.json', 'r') as f:
        input = json.load(f)
        run_benchmark = input['run_benchmark']
        benchmark_param = input['benchmark_param']
    get_fitness_vs_all_colors(run_benchmark, benchmark_param)