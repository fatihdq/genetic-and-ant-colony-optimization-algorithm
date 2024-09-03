import os
import time
import sys
import pandas as pd
import matplotlib.pyplot as plt

from algorithm.aco import antColonyOptimization

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

DEBUG = False # if DEBUG is true to print all result. Default DEBUG is false for print final result only
DatasetPath = './dataset/t5.csv'
Iteration = 10 # ACO Parameters
nAnts = 5
rho = 0.5
alpha = 1
beta = 1
InitialPheromne = 10

if __name__ == '__main__':
    origin_stdout = sys.stdout
    f = open(logFile, 'w')
    sys.stdout = f

    start_time = time.time()

    city = pd.read_csv(DatasetPath, header=None , sep=' ')

    # Start Ant Colony Optimization Algorithm process
    print("====================================== Ant Colony Optimization ======================================\n")
    print(f"Iteration: {str(Iteration)}")
    print(f"Ants: {str(nAnts)}")
    print(f"Rho: {str(rho)}")
    print(f"Alpha: {str(alpha)}")
    print(f"Beta: {str(beta)}")
    print(f"Initial Pheromne : {str(InitialPheromne)}")
    print()
    distance, bestDistances = antColonyOptimization(city, Iteration, nAnts, rho, alpha, beta, InitialPheromne, DEBUG=DEBUG)

    executionTime = time.time() - start_time
    print("EXECUTION TIME =: {hour:.4f} hour, {minutes:.4f} minutes, {seconds:.4f} seconds".format(hour = executionTime/3600, minutes = executionTime/60, seconds = executionTime))

    # Ploting ACO Result
    plt.figure(0)
    plt.plot(range(1, Iteration + 1), bestDistances)
    plt.xlabel('Iteration')
    plt.ylabel('Distance')
    plt.title('Ant Colony Optimization Result')
    plt.savefig(imageFile)

    sys.stdout = origin_stdout
    f.close()