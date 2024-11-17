import os
import time
import sys
import pandas as pd
import matplotlib.pyplot as plt

from base.city import City
from base.logger import Logger
from algorithmV3.ga import geneticAlgorithm
from algorithmV3.gaAco import gaAcoAlgorithm

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
datasetPath = "./dataset/lin318.csv"
# Algen Parameters
populationSize = 20
gaTimeCriteria = 60 # GA Criteria to stop in second
# ACO Parameters
acoTimeCriteria = 60 # ACO Criteria to stop in second
nAnts = 5
rho = 0.5
alpha = 1
beta = 1
initialPheromne = 10

if __name__ == '__main__':
    city = pd.read_csv(datasetPath, header=None , sep=' ')
    cityList = []
    for i in range(0,len(city)):
        cityList.append(City(name = city.iloc[i,0],x=city.iloc[i][1],y=city.iloc[i][2]))

    # Start Genetic Algorithm process
    log.printToLog("\n====================================== Genetica Algorithm ======================================\n")
    log.printToLog(f"Population Size: {str(populationSize)}")
    log.printToLog(f"Time Criteria: {str(gaTimeCriteria)} second")
    log.printToLog()

    gaStartTime = time.time()
    gaResult, gaDistance, gaProgress, gaNGeneration, gaTimeExecution = geneticAlgorithm(population=cityList, popSize=populationSize, startTime=gaStartTime, timeCriteria=gaTimeCriteria, log=log, DEBUG=DEBUG)
    
    # Visualize the genetic algorithm result
    plt.figure(0)
    plt.plot(gaProgress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.title('Genetica Algorithm Result')
    plt.savefig(gaImgaeFile)

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
    log.printToLog(f"Time Criteria: {str(acoTimeCriteria)} second")
    log.printToLog(f"Ants: {str(nAnts)}")
    log.printToLog(f"Rho: {str(rho)}")
    log.printToLog(f"Alpha: {str(alpha)}")
    log.printToLog(f"Beta: {str(beta)}")
    log.printToLog(f"Initial Pheromne : {str(initialPheromne)}")
    log.printToLog()

    acoStartTime = time.time()
    acoDistance, acoProgress, acoNGeneration, acoTimeExecution = gaAcoAlgorithm(city=city, nAnts=nAnts, rho=rho, alpha=alpha, beta=beta, initialPheromne=initialPheromne, routes=newPop, startTime=acoStartTime, timeCriteria=acoTimeCriteria, log=log, DEBUG=DEBUG)
    
    # Ploting ACO Result
    plt.figure(1)
    plt.plot(acoProgress)
    plt.xlabel('Iteration')
    plt.ylabel('Distance')
    plt.title('Ant Colony Optimization Result')
    plt.savefig(gaAcoImgaeFile)
    
    log.printToLog("GENETIC ALGORITHM TIME: {hour:.4f} hour, {minutes:.4f} minutes, {seconds:.4f} seconds".format(hour = gaTimeExecution/3600, minutes = gaTimeExecution/60, seconds = gaTimeExecution))
    log.printToLog("GENETIC ALGORITHM n Generation =: {nGen} \n".format(nGen = gaNGeneration))

    log.printToLog("ACO ALGORITHM TIME: {hour:.4f} hour, {minutes:.4f} minutes, {seconds:.4f} seconds".format(hour = acoTimeExecution/3600, minutes = acoTimeExecution/60, seconds = acoTimeExecution))
    log.printToLog("ACO n Generation =: {nGen} \n".format(nGen = acoNGeneration))

    log.printToLog("EXECUTION TIME =: {hour:.4f} hour, {minutes:.4f} minutes, {seconds:.4f} seconds".format(hour = (gaTimeExecution+acoTimeExecution)/3600, minutes = (gaTimeExecution+acoTimeExecution)/60, seconds = (gaTimeExecution+acoTimeExecution)))