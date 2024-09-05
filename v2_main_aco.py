import os
import time
import sys
import pandas as pd
import matplotlib.pyplot as plt

from algorithmV2.aco import antColonyOptimization
from base.logger import Logger

logFile = './logs/aco_result.txt'
imageFile = './images/aco_result.png'

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
DatasetPath = './dataset/lin318.csv'
genCriteria = 30 # ACO Parameters
nAnts = 20
rho = 0.5
alpha = 1
beta = 1
InitialPheromne = 10

if __name__ == '__main__':
    start_time = time.time()

    city = pd.read_csv(DatasetPath, header=None , sep=' ')

    # Start Ant Colony Optimization Algorithm process
    log.printToLog("====================================== Ant Colony Optimization ======================================\n")
    log.printToLog(f"Generation Criteria: {str(genCriteria)}")
    log.printToLog(f"Ants: {str(nAnts)}")
    log.printToLog(f"Rho: {str(rho)}")
    log.printToLog(f"Alpha: {str(alpha)}")
    log.printToLog(f"Beta: {str(beta)}")
    log.printToLog(f"Initial Pheromne : {str(InitialPheromne)}")
    log.printToLog()
    distance, bestDistances, nGeneration = antColonyOptimization(city, genCriteria, nAnts, rho, alpha, beta, InitialPheromne, log, DEBUG=DEBUG)

    executionTime = time.time() - start_time
    log.printToLog("EXECUTION TIME =: {hour:.4f} hour, {minutes:.4f} minutes, {seconds:.4f} seconds".format(hour = executionTime/3600, minutes = executionTime/60, seconds = executionTime))

    # Ploting ACO Result
    plt.figure(0)
    plt.plot(bestDistances)
    plt.xlabel('Iteration')
    plt.ylabel('Distance')
    plt.title('Ant Colony Optimization Result')
    plt.savefig(imageFile)