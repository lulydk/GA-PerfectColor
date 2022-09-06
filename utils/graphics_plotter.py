import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)

def get_values():
    path = "C:/Users/lulyd/Documents/GA-PerfectColor/output/graphics.txt"
    with open(path, "r") as file:
        population_size = int(file.readline())
        content = file.read()
    array = list(map(float, content.split()))
    return population_size, array

def main():
    population_size, array = get_values()
    fig, ax = plt.subplots()
    ax.set_title('Fitness through the generations')
    ax.set_ylabel('Fitness')
    ax.set_xlabel('Colors through generations')
    ax.xaxis.set_minor_locator(MultipleLocator(population_size))
    x = list(map(lambda num: num/population_size,range(len(array))))
    #ax.set_xlabel('Generations')
    #ax.xaxis.set_minor_locator(MultipleLocator(1))
    #ax.plot(x, array)
    ax.plot(array)
    plt.show()

def mainy():
    #fitness = []
    path = "C:/Users/lulyd/Documents/GA-PerfectColor/output/graphics.txt"
    with open(path, "r") as file:
        population_size = file.readline()
        content = file.read()
    array = content.split()
    numbers = list(map(float, array))
    plt.plot(numbers)
    plt.ylabel('Fitness')
    plt.xlabel('Colors through generations')
    plt.show()

if __name__ == "__main__":
    main()