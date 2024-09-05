import os
import time
import sys
import math
import shutil
import pandas as pd
import matplotlib.pyplot as plt

from base.city import City
from base.logger import Logger
from algorithmV2.ga import geneticAlgorithm
from algorithmV2.gaAco import gaAcoAlgorithm
from algorithmV2.aco import antColonyOptimization

logFile = './logs/testcaseV2_log.txt'
testcaseFile = 'testcaseV2.xlsx'
testcaseResultFile = 'testcaseV2_result.xlsx'

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
testcase['Image GA Percobaan 1'] = testcase['Image GA Percobaan 1'].astype(str)
testcase['Image GA Percobaan 2'] = testcase['Image GA Percobaan 2'].astype(str)
testcase['Image GA Percobaan 3'] = testcase['Image GA Percobaan 3'].astype(str)
testcase['Image ACO Percobaan 1'] = testcase['Image ACO Percobaan 1'].astype(str)
testcase['Image ACO Percobaan 2'] = testcase['Image ACO Percobaan 2'].astype(str)
testcase['Image ACO Percobaan 3'] = testcase['Image ACO Percobaan 3'].astype(str)
testcase['Image GA-ACO Percobaan 1'] = testcase['Image GA-ACO Percobaan 1'].astype(str)
testcase['Image GA-ACO Percobaan 2'] = testcase['Image GA-ACO Percobaan 2'].astype(str)
testcase['Image GA-ACO Percobaan 3'] = testcase['Image GA-ACO Percobaan 3'].astype(str)
testcase['Image GA-ACO 2 Line Percobaan 1'] = testcase['Image GA-ACO 2 Line Percobaan 1'].astype(str)
testcase['Image GA-ACO 2 Line Percobaan 2'] = testcase['Image GA-ACO 2 Line Percobaan 2'].astype(str)
testcase['Image GA-ACO 2 Line Percobaan 3'] = testcase['Image GA-ACO 2 Line Percobaan 3'].astype(str)
testcase['Image GA-ACO 1 Line Percobaan 1'] = testcase['Image GA-ACO 1 Line Percobaan 1'].astype(str)
testcase['Image GA-ACO 1 Line Percobaan 2'] = testcase['Image GA-ACO 1 Line Percobaan 2'].astype(str)
testcase['Image GA-ACO 1 Line Percobaan 3'] = testcase['Image GA-ACO 1 Line Percobaan 3'].astype(str)
testcase['Image GA-ACO All Percobaan 1'] = testcase['Image GA-ACO All Percobaan 1'].astype(str)
testcase['Image GA-ACO All Percobaan 2'] = testcase['Image GA-ACO All Percobaan 2'].astype(str)
testcase['Image GA-ACO All Percobaan 3'] = testcase['Image GA-ACO All Percobaan 3'].astype(str)

if __name__ == '__main__':
    for idx in range(0,len(testcase)):
        dataset = testcase.loc[idx,"Dataset"]

        # Algen Parameters
        populationSize = testcase.loc[idx,"Populasi"]
        gaGenCriteria = testcase.loc[idx,"Kriteria Generasi GA"]

        # ACO Parameters
        acoGenCriteria = testcase.loc[idx,"Kriteria Generasi ACO"]
        nAnts = testcase.loc[idx,"Jumlah Semut"]
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
 
            GAImageFilename = './tcImages/'+dataset.replace('.csv','')+'_'+str(testIdx)+'_GA_'+str(gaGenCriteria)+'.png'
            ACOImageFilename = './tcImages/'+dataset.replace('.csv','')+'_'+str(testIdx)+'_ACO_'+str(gaGenCriteria)+'.png'
            GAACOACOImageFilename = './tcImages/'+dataset.replace('.csv','')+'_'+str(testIdx)+'_GA_ACO_(ACO)_'+str(gaGenCriteria)+'.png'
            GAACO2ImageFilename = './tcImages/'+dataset.replace('.csv','')+'_'+str(testIdx)+'_GA_ACO_(2 line)_'+str(gaGenCriteria)+'.png'
            GAACO1ImageFilename = './tcImages/'+dataset.replace('.csv','')+'_'+str(testIdx)+'_GA_ACO_(1 line)_'+str(gaGenCriteria)+'.png'
            GAACOAllImageFilename = './tcImages/'+dataset.replace('.csv','')+'_'+str(testIdx)+'_GA_ACO_All_'+str(gaGenCriteria)+'.png'

            start_time = time.time()
            # Start Genetic Algorithm process
            log.printToLog("\n====================================== Genetica Algorithm ======================================\n")
            log.printToLog(f"Population Size: {str(populationSize)}")
            log.printToLog(f"Generation Criteria: {str(gaGenCriteria)}")
            log.printToLog()
            gaResult, gaDistance, gaProgress, gaNGeneration = geneticAlgorithm(population=cityList, popSize=populationSize, genCriteria=gaGenCriteria, log=log, DEBUG=DEBUG)

            end_ga_time = time.time()
            ga_time = end_ga_time - start_time

             # add first city to last index in each route
            newPop = []
            for re in gaResult:
                firstCity = re[0]
                newRoute = []
                for r in re:
                    newRoute.append(r)
                newRoute.append(firstCity)
                newPop.append(newRoute)

            # Visualize the genetic algorithm result
            plt.figure(idx+testIdx+1)
            plt.plot(gaProgress, label = 'GA')
            plt.legend()
            plt.ylabel('Distance')
            plt.xlabel('Generation')
            plt.title('Genetica Algorithm Result')
            plt.savefig(GAImageFilename)
            plt.close()

            start_time = time.time()
            # Start Ant Colony Optimization Algorithm process
            acoDistance, acoProgress, acoNGeneration = antColonyOptimization(city=city, genCriteria=acoGenCriteria, nAnts=nAnts, rho=rho, alpha=alpha, beta=beta, initialPheromne=initialPheromne, log=log, DEBUG=DEBUG)
            acoProgress = [item[0] for item in acoProgress]
            aco_time = time.time() - start_time

            # Visualize the Ant Colony Optimization Algorithm result
            plt.figure(idx+testIdx+2)
            plt.plot(acoProgress, label = 'ACO')
            plt.legend()
            plt.ylabel('Distance')
            plt.xlabel('Generation')
            plt.title('Ant Colony Optimization Result')
            plt.savefig(ACOImageFilename)
            plt.close()

            start_time = time.time()
            # Start Genetic Algorithm & Ant Colony Optimization Algorithm process
            gaAcoDistance, gaAcoProgress, gaAcoNGeneration = gaAcoAlgorithm(city=city, genCriteria=acoGenCriteria, nAnts=nAnts, rho=rho, alpha=alpha, beta=beta, initialPheromne=initialPheromne, routes=newPop, log=log, DEBUG=DEBUG)
            gaAcoProgress = [item[0] for item in gaAcoProgress]
            ga_aco_time = time.time() - start_time

            # Visualize the Genetic Algorithm & Ant Colony Optimization Algorithm result
            fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1, 2]})
            ax1.plot(gaProgress, color= '#d16747' , label = 'GA')
            ax2.plot(gaAcoProgress, color= '#383eb0', label = 'GA-ACO')
            ax1.set_ylim(min(gaProgress) - (min(gaProgress)*0.001), max(gaProgress) + (max(gaProgress)*0.001))
            ax2.set_ylim(min(gaAcoProgress) - (min(gaAcoProgress)*0.001), max(gaAcoProgress) + (max(gaAcoProgress)*0.001))
            ax1.spines.bottom.set_visible(False)
            ax2.spines.top.set_visible(False)
            ax1.xaxis.tick_top()
            ax1.tick_params(labeltop=False)
            ax2.xaxis.tick_bottom()
            fig.legend()
            fig.suptitle('GA & ACO Result')
            plt.ylabel('Distance')
            plt.xlabel('Generation')
            plt.savefig(GAACO2ImageFilename)
            plt.close()

            # Visualize the Genetic Algorithm & Ant Colony Optimization (ACO Only) Algorithm result
            plt.figure(idx+testIdx+4)
            plt.plot(gaAcoProgress, label = 'GA-ACO (ACO)')
            plt.legend()
            plt.ylabel('Distance')
            plt.xlabel('Generation')
            plt.title('GA & ACO (ACO) Result')
            plt.savefig(GAACOACOImageFilename)
            plt.close()

            # Visualize the Genetic Algorithm & Ant Colony Optimization 1 line Algorithm result            
            plt.figure(idx+testIdx+5)
            plt.plot(gaProgress + gaAcoProgress, label = 'GA-ACO')
            plt.legend()
            plt.ylabel('Distance')
            plt.xlabel('Generation, GA: '+str(gaNGeneration)+' (1-'+ str(gaNGeneration) +'), ACO: '+str(acoNGeneration)+' ('+str(gaNGeneration+1)+'-'+str(gaNGeneration+acoGenCriteria)+')')
            plt.title('GA & ACO Result')
            plt.savefig(GAACO1ImageFilename)
            plt.close()

            # Visualize the Genetic Algorithm & Ant Colony Optimization 1 line Algorithm result            
            fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1, 2]})
            ax1.plot(gaProgress, color= '#d16747' , label = 'GA')
            ax2.plot(acoProgress, color= '#6cb038', label = 'ACO')
            ax2.plot(gaAcoProgress, color= '#383eb0', label = 'GA-ACO')
            appendedProgress = acoProgress+gaAcoProgress
            ax1.set_ylim(min(gaProgress) - (min(gaProgress)*0.001), max(gaProgress) + (max(gaProgress)*0.001))
            ax2.set_ylim(min(appendedProgress) - (min(appendedProgress)*0.001), max(appendedProgress) + (max(appendedProgress)*0.001))
            ax1.spines.bottom.set_visible(False)
            ax2.spines.top.set_visible(False)
            ax1.xaxis.tick_top()
            ax1.tick_params(labeltop=False)
            ax2.xaxis.tick_bottom()
            fig.legend()
            fig.suptitle('GA, ACO, & GA-ACO Result')
            plt.ylabel('Distance')
            plt.xlabel('Generation')
            plt.savefig(GAACOAllImageFilename)
            plt.close()


            testcase.loc[idx, "Jarak GA Percobaan " + str(testIdx)] = gaDistance
            testcase.loc[idx, "Jarak ACO Percobaan " + str(testIdx)] = acoDistance
            testcase.loc[idx, "Jarak GA-ACO Percobaan " + str(testIdx)] = gaAcoDistance

            testcase.loc[idx, "Generasi GA Percobaan " + str(testIdx)] = gaNGeneration
            testcase.loc[idx, "Generasi ACO Percobaan " + str(testIdx)] = acoNGeneration
            testcase.loc[idx, "Generasi GA-ACO Percobaan " + str(testIdx)] = gaAcoNGeneration

            testcase.loc[idx, "Runtime GA Percobaan " + str(testIdx)] = round(ga_time/60,4)
            testcase.loc[idx, "Runtime ACO Percobaan " + str(testIdx)] = round(aco_time/60,4)
            testcase.loc[idx, "Runtime GA-ACO Percobaan " + str(testIdx)] = round((ga_time+ga_aco_time)/60,4)

            testcase.loc[idx, "Image GA Percobaan " + str(testIdx)] = GAImageFilename
            testcase.loc[idx, "Image ACO Percobaan " + str(testIdx)] = ACOImageFilename
            testcase.loc[idx, "Image GA-ACO Percobaan " + str(testIdx)] = GAACOACOImageFilename
            testcase.loc[idx, "Image GA-ACO 2 Line Percobaan " + str(testIdx)] = GAACO2ImageFilename
            testcase.loc[idx, "Image GA-ACO 1 Line Percobaan " + str(testIdx)] = GAACO1ImageFilename
            testcase.loc[idx, "Image GA-ACO All Percobaan " + str(testIdx)] = GAACOAllImageFilename
        
        avgDistanceGA = (testcase.loc[idx, "Jarak GA Percobaan 1"] + testcase.loc[idx, "Jarak GA Percobaan 2"] + testcase.loc[idx, "Jarak GA Percobaan 3"])/3
        avgDistanceACO = (testcase.loc[idx, "Jarak ACO Percobaan 1"] + testcase.loc[idx, "Jarak ACO Percobaan 2"] + testcase.loc[idx, "Jarak ACO Percobaan 3"])/3
        avgDistanceGAACO = (testcase.loc[idx, "Jarak GA-ACO Percobaan 1"] + testcase.loc[idx, "Jarak GA-ACO Percobaan 2"] + testcase.loc[idx, "Jarak GA-ACO Percobaan 3"])/3

        avgGenerationGA = (testcase.loc[idx, "Generasi GA Percobaan 1"] + testcase.loc[idx, "Generasi GA Percobaan 2"] + testcase.loc[idx, "Generasi GA Percobaan 3"])/3
        avgGenerationACO = (testcase.loc[idx, "Generasi ACO Percobaan 1"] + testcase.loc[idx, "Generasi ACO Percobaan 2"] + testcase.loc[idx, "Generasi ACO Percobaan 3"])/3
        avgGenerationGAACO = (testcase.loc[idx, "Generasi GA-ACO Percobaan 1"] + testcase.loc[idx, "Generasi GA-ACO Percobaan 2"] + testcase.loc[idx, "Generasi GA-ACO Percobaan 3"])/3

        testcase.loc[idx, "Rata Rata Jarak GA"] = avgDistanceGA
        testcase.loc[idx, "Rata Rata Jarak ACO"] = avgDistanceACO
        testcase.loc[idx, "Rata Rata Jarak GA-ACO"] = avgDistanceGAACO

        testcase.loc[idx, "Rata Rata Generasi GA"] = avgGenerationGA
        testcase.loc[idx, "Rata Rata Generasi ACO"] = avgGenerationACO
        testcase.loc[idx, "Rata Rata Generasi GA-ACO"] = avgGenerationGAACO

        testcase.loc[idx, "Rata Rata Runtime GA"] = (testcase.loc[idx, "Runtime GA Percobaan 1"] + testcase.loc[idx, "Runtime GA Percobaan 2"] + testcase.loc[idx, "Runtime GA Percobaan 3"])/3
        testcase.loc[idx, "Rata Rata Runtime ACO"] = (testcase.loc[idx, "Runtime ACO Percobaan 1"] + testcase.loc[idx, "Runtime ACO Percobaan 2"] + testcase.loc[idx, "Runtime ACO Percobaan 3"])/3
        testcase.loc[idx, "Rata Rata Runtime GA-ACO"] = (testcase.loc[idx, "Runtime GA-ACO Percobaan 1"] + testcase.loc[idx, "Runtime GA-ACO Percobaan 2"] + testcase.loc[idx, "Runtime GA-ACO Percobaan 3"])/3

        stdDistanceGA = math.sqrt((((testcase.loc[idx, "Jarak GA Percobaan 1"] - avgDistanceGA)**2) + ((testcase.loc[idx, "Jarak GA Percobaan 2"] - avgDistanceGA)**2) + ((testcase.loc[idx, "Jarak GA Percobaan 3"] - avgDistanceGA)**2))/2)
        stdDistanceACO = math.sqrt((((testcase.loc[idx, "Jarak ACO Percobaan 1"] - avgDistanceACO)**2) + ((testcase.loc[idx, "Jarak ACO Percobaan 2"] - avgDistanceACO)**2) + ((testcase.loc[idx, "Jarak ACO Percobaan 3"] - avgDistanceACO)**2))/2)
        stdDistanceGAACO = math.sqrt((((testcase.loc[idx, "Jarak GA-ACO Percobaan 1"] - avgDistanceGAACO)**2) + ((testcase.loc[idx, "Jarak GA-ACO Percobaan 2"] - avgDistanceGAACO)**2) + ((testcase.loc[idx, "Jarak GA-ACO Percobaan 3"] - avgDistanceGAACO)**2))/2)

        testcase.loc[idx, "Standar Deviasi Jarak GA"] = stdDistanceGA
        testcase.loc[idx, "Standar Deviasi Jarak ACO"] = stdDistanceACO
        testcase.loc[idx, "Standar Deviasi Jarak GA-ACO"] = stdDistanceGAACO

        stdGenerationGA = math.sqrt((((testcase.loc[idx, "Generasi GA Percobaan 1"] - avgGenerationGA)**2) + ((testcase.loc[idx, "Generasi GA Percobaan 2"] - avgGenerationGA)**2) + ((testcase.loc[idx, "Generasi GA Percobaan 3"] - avgGenerationGA)**2))/2)
        stdGenerationACO = math.sqrt((((testcase.loc[idx, "Generasi ACO Percobaan 1"] - avgGenerationACO)**2) + ((testcase.loc[idx, "Generasi ACO Percobaan 2"] - avgGenerationACO)**2) + ((testcase.loc[idx, "Generasi ACO Percobaan 3"] - avgGenerationACO)**2))/2)
        stdGenerationGAACO = math.sqrt((((testcase.loc[idx, "Generasi GA-ACO Percobaan 1"] - avgGenerationGAACO)**2) + ((testcase.loc[idx, "Generasi GA-ACO Percobaan 2"] - avgGenerationGAACO)**2) + ((testcase.loc[idx, "Generasi GA-ACO Percobaan 3"] - avgGenerationGAACO)**2))/2)

        testcase.loc[idx, "Standar Deviasi Generasi GA"] = stdGenerationGA
        testcase.loc[idx, "Standar Deviasi Generasi ACO"] = stdGenerationACO
        testcase.loc[idx, "Standar Deviasi Generasi GA-ACO"] = stdGenerationGAACO

    testcase.to_excel(testcaseResultFile, index=False)