import sys
import os
import time
import pandas as pd
import matplotlib.pyplot as plt

from algorithm.ga import geneticAlgorithm
from base.city import City
from base.logger import Logger

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

log = Logger(logFile)
DEBUG = False # if DEBUG is true to print all result. Default DEBUG is false for print final result only
datasetPath = "./dataset/t5.csv"
populationSize = 5 # Genetic Algorithm Parameters
generation = 50

if __name__ == '__main__':
    start_time = time.time()

    city = pd.read_csv(datasetPath, header=None , sep=' ')
    cityList = []
    for i in range(0,len(city)):
        cityList.append(City(name = city.iloc[i,0],x=city.iloc[i][1],y=city.iloc[i][2]))

    # Start Genetic Algorithm process
    log.printToLog("\n====================================== Genetica Algorithm ======================================\n")
    log.printToLog(f"Population Size: {str(populationSize)}")
    log.printToLog(f"Generation: {str(generation)}")
    log.printToLog()

    finalPopulation, bestDistance, progress = geneticAlgorithm(population=cityList, popSize=populationSize, generations=generation, log=log, DEBUG=DEBUG)

    executionTime = time.time() - start_time
    log.printToLog("EXECUTION TIME =: {hour:.4f} hour, {minutes:.4f} minutes, {seconds:.4f} seconds".format(hour = executionTime/3600, minutes = executionTime/60, seconds = executionTime))

    # Visualize the genetic algorithm result
    plt.figure(0)
    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.title('Genetica Algorithm Result')
    plt.savefig(imageFile)