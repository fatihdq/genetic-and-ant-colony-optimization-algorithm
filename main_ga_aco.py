import os
import time
import sys
import pandas as pd
import matplotlib.pyplot as plt

from base.city import City
from base.logger import Logger
from algorithm.ga import geneticAlgorithm
from algorithm.gaAco import gaAcoAlgorithm

logFile = './logs/ga_aco_result.txt'
gaImgaeFile = './images/ga_result.png'
gaAcoImgaeFile = './images/ga_aco_result.png'


if not os.path.exists('./logs'):
    os.mkdir('./logs')
if not os.path.exists('./images'):
    os.mkdir('./images')

if os.path.exists(logFile):
    os.remove(logFile)
if os.path.exists(gaImgaeFile):
    os.remove(gaImgaeFile)
if os.path.exists(gaAcoImgaeFile):
    os.remove(gaAcoImgaeFile)

log = Logger(logFile)
DEBUG = False # if DEBUG is true to print all result. Default DEBUG is false for print final result only
datasetPath = "./dataset/t5.csv"
# Algen Parameters
populationSize = 5
generation = 50
# ACO Parameters
iteration = 10
nAnts = 5
rho = 0.5
alpha = 1
beta = 1
initialPheromne = 10

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
    gaResult, gaDistance, gaProgress = geneticAlgorithm(population=cityList, popSize=populationSize, generations=generation, log=log, DEBUG=DEBUG)
    
    # Visualize the genetic algorithm result
    plt.figure(0)
    plt.plot(gaProgress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.title('Genetica Algorithm Result')
    plt.savefig(gaImgaeFile)

    end_algen_time = time.time()
    algo_time = end_algen_time - start_time

    # add first city to last index in each route
    newPop = []
    for r in gaResult:
        firstCity = r[0]
        newRoute = []
        for r2 in r:
            newRoute.append(r2)
        newRoute.append(firstCity)
        newPop.append(newRoute)

    # Start Ant Colony Optimization Algorithm process
    log.printToLog("\n\n====================================== Ant Colony Optimization ======================================\n")
    log.printToLog(f"Iteration: {str(iteration)}")
    log.printToLog(f"Ants: {str(nAnts)}")
    log.printToLog(f"Rho: {str(rho)}")
    log.printToLog(f"Alpha: {str(alpha)}")
    log.printToLog(f"Beta: {str(beta)}")
    log.printToLog(f"Initial Pheromne : {str(initialPheromne)}")
    log.printToLog()

    acoDistance, acoProgress = gaAcoAlgorithm(city=city, iteration=iteration, nAnts=nAnts, rho=rho, alpha=alpha, beta=beta, initialPheromne=initialPheromne, routes=newPop, log=log, DEBUG=DEBUG)
    
    # Ploting ACO Result
    plt.figure(1)
    plt.plot(range(1, iteration + 1), acoProgress)
    plt.xlabel('Iteration')
    plt.ylabel('Distance')
    plt.title('Ant Colony Optimization Result')
    plt.savefig(gaAcoImgaeFile)
    
    aco_time = time.time() - end_algen_time
    executionTime = time.time() - start_time

    log.printToLog("GENETIC ALGORITHM TIME: {hour:.4f} hour, {minutes:.4f} minutes, {seconds:.4f} seconds".format(hour = algo_time/3600, minutes = algo_time/60, seconds = algo_time))
    log.printToLog("ACO ALGORITHM TIME: {hour:.4f} hour, {minutes:.4f} minutes, {seconds:.4f} seconds".format(hour = aco_time/3600, minutes = aco_time/60, seconds = aco_time))
    log.printToLog("EXECUTION TIME =: {hour:.4f} hour, {minutes:.4f} minutes, {seconds:.4f} seconds".format(hour = executionTime/3600, minutes = executionTime/60, seconds = executionTime))