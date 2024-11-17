import os
import time
import sys
import pandas as pd
import matplotlib.pyplot as plt

from algorithmV3.aco import antColonyOptimization
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
nAnts = 200
rho = 0.5
alpha = 1
beta = 1
InitialPheromne = 10
timeCriteria = 60 # Criteria to stop in second

if __name__ == '__main__':


    city = pd.read_csv(DatasetPath, header=None , sep=' ')

    # Start Ant Colony Optimization Algorithm process
    log.printToLog("====================================== Ant Colony Optimization ======================================\n")
    log.printToLog(f"Ants: {str(nAnts)}")
    log.printToLog(f"Rho: {str(rho)}")
    log.printToLog(f"Alpha: {str(alpha)}")
    log.printToLog(f"Beta: {str(beta)}")
    log.printToLog(f"Initial Pheromne : {str(InitialPheromne)}")
    log.printToLog(f"Time Criteria: {str(timeCriteria)} Second")
    log.printToLog()

    start_time = time.time()
    distance, bestDistances, nGeneration, timeExecution = antColonyOptimization(city, nAnts, rho, alpha, beta, InitialPheromne, start_time, timeCriteria, log, DEBUG=DEBUG)

    log.printToLog("EXECUTION TIME =: {hour:.4f} hour, {minutes:.4f} minutes, {seconds:.4f} seconds".format(hour = timeExecution/3600, minutes = timeExecution/60, seconds = timeExecution))
    log.printToLog("n Generation =: {nGen} ".format(nGen = nGeneration))

    # Ploting ACO Result
    plt.figure(0)
    plt.plot(bestDistances)
    plt.xlabel('Iteration')
    plt.ylabel('Distance')
    plt.title('Ant Colony Optimization Result')
    plt.savefig(imageFile)