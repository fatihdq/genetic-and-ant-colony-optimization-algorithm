# Genetic Algorithm & Ant Colony Optimization
This repository is for calculating the TSP (Traveling Salesman Problem) algorithm using Genetic Algorithms, Ant Colony Optimization or both.

## Prerequisite
- Python  3 / Jupyter Notebook
- Python venv
- Pip 3

## How to use

### Dataset 
You can use a dataset in CSV format: city names (numbers), x coordinates (float), y coordinates (float), with space separator

example data in dataset directory

### Jupyter Notebook or Common Python
If you prefer to use a Jupyter notebook, you can use the ipynb file in the notebooks directory
- geneticAlgorithm.ipynb
- antColonyOptimization.ipynb
- geneticACOAlgorithm.ipynb

To run one of the algorithms you can use the following python file:
- main_ga.py
- main_aco.py
- main_ga_aco.py


### Variable to setup the algorithm parameters
dateset
```
datasetPath = "./dataset/t5.csv"
```

Genetic Algorithm Parameters
```
populationSize = 10
generation = 10
```

Ant Colony Optimization
```
iteration = 10
nAnts = 5
rho = 0.5
alpha = 1
beta = 1
initialPheromne = 10
```

to print all the algorithm process
``` 
DEBUG = TRUE
``` 
to print the final result of the algorithm only
```
DEBUG = FALSE //default
```  

### Result
- ./logs: print out the algorithm process log in .txt file
- ./images: to visualize the algorithm result in .png file

## Test Case 
The format that must be prepared is as in `testcase.xlsx` and the results are as in `testcase_result.xlsx`.
You can follow this format or modify it according to your needs

you can use notebook `./notebooks/testcaseGA-ACO.ipynb` or `./main_testcase.py`,  