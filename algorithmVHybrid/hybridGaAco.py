import numpy as np 
import time 
import random

from base.city import City
from base.route import Route

np.seterr(divide='ignore', invalid='ignore')

def rankRoutes(population):
    fitnessResults = []
    rankRoute = {}

    #Determine fitness each individual in population
    for i in range(0, len(population)):
        fitnessResult = {}
        fitnessResult['route'] = population[i]
        fitnessResult['fitness'] = Route(population[i]).routeFitness()
        fitnessResults.append(fitnessResult)

    #Sorting based on fitness value
    sortedFitness = sorted(fitnessResults, key=lambda x: x['fitness'], reverse=True)

    for i in range(0, len(sortedFitness)):
        rankRoute[i] = sortedFitness[i]['route']

    return rankRoute

def selection(population, log, DEBUG=False):
    selection = []
    #Take first 2  the best individuals
    for i in range(0,2):
        selection.append(population[i])
        if DEBUG:
            log.printToLog("seleksi ke-" + str(i+1) + " " + str(Route(selection[i]).printCity()) + "\n" +
                " Jarak = " + str(Route(selection[i]).routeDistance()) + "\n" + " Fitness = " + str(
                Route(selection[i]).routeFitness()))
    return selection


def tabulist(selectionResults, tabulist):
    isTabulist1 = False
    isTabulist2 = False
    isTabulist = False

    #Check tabulist
    for j in range(0,len(tabulist)):
        if selectionResults[0] == tabulist[j]:
            isTabulist1 = True
        if selectionResults[1] == tabulist[j]:
            isTabulist2 = True

    if isTabulist1 == False:
        tabulist.append(selectionResults[0])
    if isTabulist2 == False:
        tabulist.append(selectionResults[1])

    if isTabulist1 == True and isTabulist2 == True:
        isTabulist = True

    return isTabulist,tabulist

def crossover(parent1, parent2, tab, log, DEBUG=False):
    childP1 = []
    childP2 = []
    child = []

    # randomizes the gene number to be carried out crossover
    # if tabulis is true then the crossover result is the same as parent1 (best individual)
    if tab == True:
        geneA = 0
        geneB = len(parent1)-1
    else:
        geneA = random.randint(1, len(parent1)-1)
        geneB = random.randint(1, len(parent1)-1)
        # Gene A and Gene B do not have the same value
        while geneA == geneB:
            geneB = random.randint(1, len(parent1)-1)

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)
    
    if DEBUG:
        log.printToLog("stargene = "+str(startGene+1)+", endGene = "+str(endGene+1))

    for i in range(startGene, endGene+1):
        childP1.append(parent1[i])

    for item in parent2:
        if item not in childP1:
            childP2.append(item)

    #Crossover Result
    idxChild1 = 0
    idxChild2 = 0
    for i in range(len(parent1)):
      if i >= startGene and i <= endGene:
        child.append(childP1[idxChild1])
        idxChild1 += 1
      else:
        child.append(childP2[idxChild2])
        idxChild2 += 1

    return child

def mutate(individual, log, DEBUG=False):
    #randomizes the gene number to be exchanged
    swapped = random.randint(1, len(individual)-1)
    swapWith = random.randint(1, len(individual)-1)
    #swapped and swapWith cannot have the same value
    while swapped == swapWith:
        swapWith = random.randint(1, len(individual)-1)

    city1 = individual[swapped]
    city2 = individual[swapWith]

    if DEBUG:
        log.printToLog("swapped = "+str(swapped+1) + " , swap with = " + str(swapWith+1))

    #hasil mutasi
    individual[swapped] = city2
    individual[swapWith] = city1
    return individual

def updateGeneration(population, popsize, mutate, log, DEBUG=False):
    generasibaru =[]
    #combining populations with mutation results to create a new generation
    for i in range(0,popsize):
        generasibaru.append(population[i])

    #replace the individual with the smallest fitness (last index) with the mutation result if the mutation result is greater
    if Route(mutate).routeFitness() >= Route(generasibaru[-1]).routeFitness():
      generasibaru[popsize-1] =mutate

    return generasibaru

def hybridGaAco(city, nAnts, rho, alpha, beta, initialPheromne, startTime, timeCriteria, log, DEBUG=False):
    cityList = []
    for i in range(0, len(city)):
        cityList.append(City(name = city.iloc[i,0],x=city.iloc[i][1],y=city.iloc[i][2]))

    distances = np.zeros((len(cityList), len(cityList)))
    visibility = np.zeros((len(cityList), len(cityList)))

    # Initialization Pheromne
    pheromne = initialPheromne * np.ones((len(cityList), len(cityList)))
    log.printToLog("Initial Pheromne")
    log.printToLog("--------------------------------")
    log.printToLog("Initail City | Destination City | New Pheromne")
    for row in range(len(cityList)):
        for col in range (len(cityList)):
            distance = cityList[row].distance(cityList[col])
            distances[row, col] = distance
            visibility[row, col] = 1/distance  if distance != 0 else 0
            if col > row:
                log.printToLog(f"{row + 1}             | {col + 1}               | {pheromne[row, col]:.4f}")
    log.printToLog("------------------------------------------\n")

    bestRoute = None
    bestDistance = float('inf')
    bestDistances = []

    tabulistResult = []
    timeExecution = 0
    looping = True
    idx = 0
    while looping:
        if DEBUG or idx == 0:
            log.printToLog(f"=========================== Iteration {idx+1} ============================")

         # Randomize the first city each ants
        initialCitiesIdx = np.random.permutation(len(cityList))
        totalDistance = np.zeros((nAnts, 1))
        routes = []
        for i in range(nAnts):
            route = []
            route.append(cityList[initialCitiesIdx[i]]) # Assign first city to routes
            visibilityTemp = np.array(visibility)

            for j in range(len(cityList)-1):
                # Calculate Probabilities
                currentLocation = int(route[j].name) -1
                visibilityTemp[:, currentLocation] = 0

                pFeature = np.power(pheromne[currentLocation, :], beta)
                vFeature = np.power(visibilityTemp[currentLocation, :], alpha)
                features = np.multiply(pFeature, vFeature)
                total = np.sum(features)
                probabilities = features/total
                
                if DEBUG:
                    log.printToLog(f"Ant {i + 1}: {route}")
                    log.printToLog("---------------------")
                    log.printToLog("City  | Probability |")
                    for k in range(len(cityList)):
                        log.printToLog(f"{k + 1}     | {probabilities[k]:.4f}       |")
                    log.printToLog("---------------------")

                # Choose next city with highest probability
                nextCityIdx = np.argmax(probabilities)
                route.append(cityList[nextCityIdx]) # Add next city to route
            if DEBUG:
                log.printToLog(f"Ant {i + 1}: {route}")

            routes.append(route)
            if DEBUG:
                log.printToLog("\n====================\n")
        
        ### GA process
        if (DEBUG) or (idx == 0):
            log.printToLog("===========================     Ant Colony Result     ===============================================================>")

        # Sort each individual in population based on ranking
        rankRoute = rankRoutes(routes)
        routes = []
        for i in range(0,nAnts):
            routes.append(rankRoute[i])
            if (DEBUG) or (idx == 0):
                log.printToLog("Populasi/Ant ke-" + str(i+1) + " " + str(rankRoute[i]) +
                    " Jarak = " + str(Route(rankRoute[i]).routeDistance()) + " Fitness = " + str(
                    Route(rankRoute[i]).routeFitness()))
        if (DEBUG) or (idx == 0):
            log.printToLog("=====================================================================================================================>\n\n")
        
        #Selection process
        selectionResults = selection(routes, log, DEBUG)
        #Check Tabulist
        tab, tabulistResult = tabulist(selectionResults, tabulistResult)

        #Crossover if the tabulist true
        crossoverResult = crossover(selectionResults[0], selectionResults[1], tab, log, DEBUG)

        if (DEBUG) or (idx == 0):
            log.printToLog("Crosover Result")
            log.printToLog("==========================================================================================>")
            log.printToLog("seleksi 1 = " + str(crossoverResult))
            log.printToLog("==========================================================================================>")

        #Mutate Process
        children = mutate(crossoverResult, log, DEBUG)
        if (DEBUG) or (idx == 0):
            log.printToLog("hasil mutasi = " + str(children) + " Jarak = " + str(Route(children).routeDistance()) + " Fitness = " + str(
                Route(children).routeFitness()))
            log.printToLog("==========================================================================================>")
        
        #Update Generation
        routesTemp = updateGeneration(routes, nAnts, children, log, DEBUG)
        routes = routesTemp

        if (DEBUG) or (idx == 0):
            log.printToLog("===========================  Genetic Algorithm Result   ===============================================================>")

        for i in range(nAnts):
            firstCity = routes[i][0]
            routes[i].append(firstCity)
            totalDistance[i] = Route(routes[i]).routeDistance()

            if (DEBUG) or (idx == 0):
                log.printToLog("Populasi/Ant ke-" + str(i+1) + " " + str(Route(routes[i]).printCity()) +
                    " Jarak = " + str(Route(routes[i]).routeDistance()) + " Fitness = " + str(
                    Route(routes[i]).routeFitness()))
            
        
        if (DEBUG) or (idx == 0):
            log.printToLog("=======================================================================================================================>\n\n")

        # Search the best routes
        distanceMinIdx = np.argmin(totalDistance)
        distanceMin = totalDistance[distanceMinIdx]
        if distanceMin < bestDistance:
            bestDistance = distanceMin
            bestRoute = routes[distanceMinIdx]
        bestDistances.append(bestDistance)

        if (time.time() - startTime) >= timeCriteria:
            timeExecution = time.time() - startTime
            looping = False

        # Update pheromne
        pheromne = (1 - rho) * pheromne # Evaporation
        for i in range(nAnts):
            delta = 1 / totalDistance[i][0] # Delta Pheromne
            for j in range(len(cityList)):
                pheromne[int(routes[i][j].name) - 1, int(routes[i][j+1].name) - 1] += delta
                pheromne[int(routes[i][j + 1].name) - 1, int(routes[i][j].name) - 1] += delta

        if DEBUG == False and looping == False:
            log.printToLog(f"=========================== Iteration {idx+1} ============================")     

        if DEBUG or looping == False or idx == 0 :
            log.printToLog("Update Pheromne")
            log.printToLog("--------------------------------")
            log.printToLog("Initail City | Destination City | New Pheromne")
        for i in range(len(cityList)):
            for j in range(i+1, len(cityList)):
                pheromneValue = pheromne[i, j]
                if DEBUG or looping == False or idx == 0:
                    log.printToLog(f"{i + 1}             | {j + 1}               | {pheromneValue:.4f}")
        if DEBUG or looping == False or idx == 0:
            log.printToLog("------------------------------------------\n")
        
        idx += 1

    nGeneration = idx
    log.printToLog(f"The best routes: {Route(bestRoute).printCity()} | Total Distance = {bestDistance[0]:.4f}")
    log.printToLog(f"total generation: {nGeneration}")
    return bestDistances[-1], bestDistances, nGeneration, timeExecution



            

        


        



        


