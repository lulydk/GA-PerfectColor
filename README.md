# Genetic Algorithm: Perfect Color

Given a **target color** and a *set of colors* (these will be referred as **color palette**), find the best way to mix proportions of every color in the palette and get the closest resulting color that matches the target the most, by making use of a genetic algorithm (GA).

# Configuration

## Installation guide

1. **Clone the repository.**
    
    ```bash
    git clone https://github.com/lulydk/GA-PerfectColor.git
    cd GA-PerfectColor
    ```
    
2. **Create a Python virtual environment.**
    
    ```bash
    python -m venv ga_color
    ```
    
3. **Activate the virtual environment and install the dependencies.**
    1. For Windows
        
        ```bash
        ./ga_color/Scripts/Activate.ps1
        pip install -r requirements.txt
        ```
        
    2. For Linux / MacOS
        
        ```bash
        ./ga_color/Scripts/activate
        pip install -r requirements.txt
        ```
        
4. **Run the program.**
    1. Simulation.
        
        ```bash
        python .\main.py
        ```
        
    2. Graphics plotter.
        
        ```bash
        python .\utils\graphics_plotter.py
        ```
        

## Inputs

The program (that is, the wrapper that runs the simulation, stores the data, and process it) has its parameters, and the genetic algorithm used *in* the program also has its own. The latter will be referred as *hyperparameters*.

Let’s analyze the file used to keep track of all these parameters: `config.json`

Since JSON is a data-only format, it doesn’t support comments. That’s why the turnaround was to put the comments as pseudo data, starting their names with underscores. That way, we can have easy access to the different options of a parameter.

```json
{
    "target_color": [100, 25, 100],

    "work_with_rgb": 1,
    "random_palette": 1,
    "color_palette_file": "color_palette.txt",

    "run_benchmark": 1,
    "benchmark_param": 5,

    "hyperparameters" : {
				"___implementation_options": "fill-all, fill-parent",
        "implementation": "fill-all",

        "___selection_options": "elite, roulette, det-tournament",
        "selection": "roulette",
        "population_n": 100,
        "individuals_k": 70,

        "___tornament_param": "",
        "individuals_m": 100,

        "cross_prob": 0.9,

        "mutation_prob": 0.9,

        "cut_criteria": {
            "___cut_options": "generations, threshold, exhaustion",
            "method": "generations",
            "max_num_generations": 100,
            "delta_treshold": 2
        }
    }
}
```

### **Program parameters**

- The `target_color` in RGB coordinates.
- The color palette:
    - Generated randomly by setting the value of `random_palette` to 1. The RGB values for every color can be found in `color_palette_file`, with the size of the palette being a random number between 3 and 100.
    - With `random_palette` set to 0, the contents in `color_palette_file` will be parsed as a list of lists with RGB coordinates.
        
        ```
        128 200 193
        113 50 219
        76 143 249
        ...
        ```
        
- The color space:
    - If `work_with_rgb` is set to 1, it will run the simulation with the given coordinates.
    - If `work_with_rgb` is set to 0, it will transform all the RGB values to its equivalent in the [CIELAB color space](https://en.wikipedia.org/wiki/CIELAB_color_space#:~:text=The%20CIELAB%20color%20space%2C%20also,prevent%20confusion%20with%20Hunter%20Lab.)) with L*a*b* coordinates, and work with them through the whole simulation.
- Benchmarking:
    - If `run_benchmark` is set to 1, it will run the simulation the number of times indicated by `benchmark_param`.

### **GA hyperparameters**

- Setting the `implementation` approach:
    
    With K = `individuals_k`, and Population Size = `population_n`.
    
    - With “fill-all”, if we generated K children from K parents, the new generation will be selected from a pool with the current generation and the K children.
    - With “fill-parent”, if we generated K children from K parents:
        - If the population size is smaller than the number of children obtained, the new generation is selected from those children only.
        - If the population size is greater or equal to the number of children obtained, the new generation will be the K children and the number of individuals needed to reach the population size, selected randomly from of the current generation.
- Setting the `selection` method:
    
    With K = `individuals_k`, and Population Size = `population_n`.
    
    - With “elite”, we take K individuals from the current generation by ranking them by their fitness and choosing the fitter individuals more times than the others, until the K number is reached.
    - With the “roulette” implementation we try to imitate the object that gives this method its name: the fitter the individual, the bigger the space they take in the roulette. This decreases the chances to choose an unfit individual, while still giving them a chance to be selected.
    - With the “det-tournament” option, we randomly take `individuals_m` individuals from the whole population, and then keep the fitter. This process is repeated until K individuals are chosen.
- Tuning the crossover method:
    - With the `cross_prob` parameter, we control the chances for two parents to carry out a single-point crossover or create children that are exact copies of them.
        - Single-point crossover: choosing a random locus, swap the alleles from that point onwards.
- Set the mutation rate with the `mutation_prob` parameter.
    - Given the structure of our genotype (explained in the next section), the chosen mutation selects new random values for every gene to replace the current ones.
- Selecting the `cut_criteria.method` to stop the simulation:
    - With the “generations” option, stop after `max_num_generations`.
    - With the “threshold” option, stop after the distance to the target is less than `delta_threshold`.
    - With the “exhaustion” option, stop after `max_num_generations` have passed without improving the result.

# Genetic Algorithm

## Chromosome structure

The **gene** represents the *proportion of a single input color in the mix*. A **chromosome** is a *sequence of genes* with the restricting condition that *all the values of its genes add up to one*.

An example of a 4 genes chromosome, based on a color palette with four colors, has the form:

| Color 1 (Gene 1) | Color 2 (Gene 2) | Color 3 (Gene 3) | Color 4 (Gene 4) |
| --- | --- | --- | --- |
| 0.25 | 0.15 | 0.10 | 0.5 |

## Evaluation of fitness

First, the element of the population is converted to color coordinates in the chosen color space, based on the recipe described by the proportions of the chromosome.

$$
\begin{bmatrix}
X\\ 
Y\\ 
Z
\end{bmatrix} = \sum_{i=1}^{\#genes} \alpha_i \begin{bmatrix}
X_i\\ 
Y_i\\ 
Z_i
\end{bmatrix}
$$

- $X,Y,Z$ being $R,G,B$ or $L*,a*,b*$ based on the selected color space.
- $\alpha_i$ being the proportion of the Gene $i$ in the mix.

After getting the coordinates, the similarity of the resulting color to the target color can be expressed as the Euclidean distance between them:

$$
\Delta E=\sqrt{(\Delta X)^2+(\Delta Y)^2+(\Delta Z)^2}
$$

Lastly, the fitness function can be expressed as follows:

$$
fitness=\frac{1}{\Delta E + \varepsilon} \cdot \omega
$$

- $\varepsilon$ is a small floating-point number to avoid dividing by zero.
- $\omega$ has the form $10^x$, and acts as a multiplier. It allows us to work with bigger numbers when the $\Delta E$ values are expected to be large.