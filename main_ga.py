import sys
import os
import time
import pandas as pd
import matplotlib.pyplot as plt

from algorithm.geneticAlgorithm import geneticAlgorithm
from base.city import City

logFile = './logs/ga_result.txt'
imageFile = './images/ga_result.png'

if not os.path.exists('./logs'):
    os.mkdir('./logs')
if not os.path.exists('./images'):
    os.mkdir('./images')

if os.path.exists(logFile):
    os.remove(logFile)
if os.path.exists(imageFile):
    os.remove(imageFile)

DEBUG = False # if DEBUG is true to print all result. Default DEBUG is false for print final result only
datasetPath = "./dataset/t5.csv"
populationSize = 5 # Genetic Algorithm Parameters
generation = 50

if __name__ == '__main__':
    origin_stdout = sys.stdout
    f = open(logFile, 'w')
    sys.stdout = f

    start_time = time.time()

    city = pd.read_csv(datasetPath, header=None , sep=' ')
    cityList = []
    for i in range(0,len(city)):
        cityList.append(City(name = city.iloc[i,0],x=city.iloc[i][1],y=city.iloc[i][2]))

    # Start Genetic Algorithm process
    print("\n====================================== Genetica Algorithm ======================================\n")
    print(f"Population Size: {str(populationSize)}")
    print(f"Generation: {str(generation)}")
    print()

    finalPopulation, bestDistance, progress = geneticAlgorithm(population=cityList, popSize=populationSize, generations=generation, DEBUG=DEBUG)

    executionTime = time.time() - start_time
    print("EXECUTION TIME =: {hour:.4f} hour, {minutes:.4f} minutes, {seconds:.4f} seconds".format(hour = executionTime/3600, minutes = executionTime/60, seconds = executionTime))

    # Visualize the genetic algorithm result
    plt.figure(0)
    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.title('Genetica Algorithm Result')
    plt.savefig(imageFile)

    sys.stdout = origin_stdout
    f.close()