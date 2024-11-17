import os
import time
import sys
import math
import shutil
import pandas as pd
import matplotlib.pyplot as plt

from base.city import City
from base.logger import Logger
from algorithmVHybrid.hybridGaAco import hybridGaAco

logFile = './logs/testcaseVHybrid_log.txt'
testcaseFile = 'testcaseVHybrid.xlsx'
testcaseResultFile = 'testcaseVHybrid_result.xlsx'

if not os.path.exists('./logs'):
    os.mkdir('./logs')
if os.path.exists(logFile):
    os.remove(logFile)
if os.path.exists('tcImages'):
    shutil.rmtree('tcImages')
    os.mkdir('tcImages')
else:
    os.mkdir('tcImages')
if os.path.exists(testcaseResultFile):
    os.remove(testcaseResultFile)

log = Logger(logFile)

DEBUG = False # if DEBUG is true to print all result. Default DEBUG is false for print final result only

testcase = pd.read_excel(testcaseFile)
testcase['Image Percobaan 1'] = testcase['Image Percobaan 1'].astype(str)
testcase['Image Percobaan 2'] = testcase['Image Percobaan 2'].astype(str)
testcase['Image Percobaan 3'] = testcase['Image Percobaan 3'].astype(str)

if __name__ == '__main__':
    for idx in range(0,len(testcase)):
        dataset = testcase.loc[idx,"Dataset"]
        number = testcase.loc[idx,"No."]

        # Algen ACO Parameters
        timeCriteria = testcase.loc[idx,"Kriteria Waktu"]
        nAnts = testcase.loc[idx,"Jumlah Semut/Populasi"] ## Ant or Population
        rho = testcase.loc[idx,"Rho"]
        alpha = testcase.loc[idx,"Alpha"]
        beta = testcase.loc[idx,"Beta"]
        initialPheromne = testcase.loc[idx,"Pheromone Awal"]

        city = pd.read_csv("./dataset/"+dataset, header=None, sep=' ')
        cityList = []
        for i in range(0,len(city)):
            cityList.append(City(name = city.iloc[i,0],x=city.iloc[i][1],y=city.iloc[i][2]))

        
        for testIdx in range(1, 4):
            log.progressBar((idx*3)+testIdx, (len(testcase)*3), idx, dataset, testIdx)
 
            imageFilename = './tcImages/'+dataset.replace('.csv','')+'_'+str(testIdx)+'_HYBRID_'+str(number)+'.png'



            startTime = time.time()
            # Start Ant Colony Optimization Algorithm process
            distance, progress, nGeneration, timeExecution = hybridGaAco(city=city, nAnts=nAnts, rho=rho, alpha=alpha, beta=beta, initialPheromne=initialPheromne, startTime=startTime, timeCriteria=timeCriteria, log=log, DEBUG=DEBUG)
            progress = [item[0] for item in progress]

            # Visualize the Ant Colony Optimization Algorithm result
            plt.figure(idx+testIdx+2)
            plt.plot(progress, label = 'Hybrid GA-ACO')
            plt.legend()
            plt.ylabel('Distance')
            plt.xlabel('Generation')
            plt.title('Hybrid GA-ACO Algorithm')
            plt.savefig(imageFilename)
            plt.close()


            testcase.loc[idx, "Jarak Percobaan " + str(testIdx)] = distance
            testcase.loc[idx, "Generasi Percobaan " + str(testIdx)] = nGeneration
            testcase.loc[idx, "Runtime Percobaan " + str(testIdx)] = round(timeExecution/60,4)
            testcase.loc[idx, "Image Percobaan " + str(testIdx)] = imageFilename
    
        
        avgDistance = (testcase.loc[idx, "Jarak Percobaan 1"] + testcase.loc[idx, "Jarak Percobaan 2"] + testcase.loc[idx, "Jarak Percobaan 3"])/3
        avgGeneration = (testcase.loc[idx, "Generasi Percobaan 1"] + testcase.loc[idx, "Generasi Percobaan 2"] + testcase.loc[idx, "Generasi Percobaan 3"])/3

        testcase.loc[idx, "Rata Rata Jarak"] = avgDistance
        testcase.loc[idx, "Rata Rata Generasi"] = avgGeneration
        testcase.loc[idx, "Rata Rata Runtime"] = (testcase.loc[idx, "Runtime Percobaan 1"] + testcase.loc[idx, "Runtime Percobaan 2"] + testcase.loc[idx, "Runtime Percobaan 3"])/3
        
        stdDistance = math.sqrt((((testcase.loc[idx, "Jarak Percobaan 1"] - avgDistance)**2) + ((testcase.loc[idx, "Jarak Percobaan 2"] - avgDistance)**2) + ((testcase.loc[idx, "Jarak Percobaan 3"] - avgDistance)**2))/2)
        testcase.loc[idx, "Standar Deviasi Jarak"] = stdDistance

        stdGeneration = math.sqrt((((testcase.loc[idx, "Generasi Percobaan 1"] - avgGeneration)**2) + ((testcase.loc[idx, "Generasi Percobaan 2"] - avgGeneration)**2) + ((testcase.loc[idx, "Generasi Percobaan 3"] - avgGeneration)**2))/2)
        testcase.loc[idx, "Standar Deviasi Generasi"] = stdGeneration

    testcase.to_excel(testcaseResultFile, index=False)