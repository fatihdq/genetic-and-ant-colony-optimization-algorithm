import numpy as np
import time

from base.city import City
    
def antColonyOptimization(city, nAnts, rho, alpha, beta, initialPheromne, startTime, timeCriteria, log, DEBUG=False):
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


    routes = np.ones((nAnts, len(cityList)+1), dtype=int)
    bestRoute = None
    bestDistance = float('inf')
    bestDistances = []

    # ACO Iteration
    timeExecution = 0
    looping = True
    idx = 0
    while looping:
        if DEBUG or idx == 0:
            log.printToLog(f"=========================== Iteration {idx+1} ============================")
        antAndDistanceStr = ""
    
        # Randomize the first city each ants
        initialCitiesIdx = np.random.permutation(len(cityList))
        totalDistance = np.zeros((nAnts, 1))
        for i in range(nAnts):
            distance = 0
            routes[i, 0] = initialCitiesIdx[i] + 1 # Assign first city to routes
            visibilityTemp = np.array(visibility)

            for j in range(len(cityList)-1):

                # Calculate Probabilities
                currentLocation = int(routes[i, j] -1)
                visibilityTemp[:, currentLocation] = 0

                pFeature = np.power(pheromne[currentLocation, :], beta)
                vFeature = np.power(visibilityTemp[currentLocation, :], alpha)
                features = np.multiply(pFeature, vFeature)
                total = np.sum(features)
                probabilities = features/total
                
                if DEBUG:
                    log.printToLog(f"Ant {i + 1}: {routes[i, :]}")
                    log.printToLog("---------------------")
                    log.printToLog("City  | Probability |")
                    for k in range(len(cityList)):
                        log.printToLog(f"{k + 1}     | {probabilities[k]:.4f}       |")
                    log.printToLog("---------------------")

                # Choose next city with highest probability
                nextCityIdx = np.argmax(probabilities)
                routes[i, j+1] = nextCityIdx + 1 # Add next city to route

                distance += distances[int(routes[i, j]) - 1, int(routes[i, j+1]) - 1]

            routes[i, -1] = routes[i, 0] # Back to first City
            if DEBUG:
                log.printToLog(f"Ant {i + 1}: {routes[i, :]}")

            # Calculate last city to first city
            distance += distances[int(routes[i, -2]) - 1, int(routes[i, -1]) - 1]
            totalDistance[i] = distance
            antAndDistanceStr += f"Ant {i+1}: {'-'.join(map(str, map(int, routes[i, :])))} | Distance = {totalDistance[i, 0]:.4f}\n"

            if DEBUG:
                log.printToLog("\n====================\n")

        if DEBUG:
            log.printToLog(f"Iteration {idx+1} Result: ")
            log.printToLog(antAndDistanceStr)


        # Search the best routes
        distanceMinIdx = np.argmin(totalDistance)
        distanceMin = totalDistance[distanceMinIdx]
        if distanceMin < bestDistance:
            bestDistance = distanceMin
            bestRoute = routes[distanceMinIdx, :]

        bestDistances.append(bestDistance)
        
        if (time.time() - startTime) >= timeCriteria:
            timeExecution = time.time() - startTime
            looping = False

        # Update pheromne
        pheromne = (1 - rho) * pheromne # Evaporation
        for i in range(nAnts):
            delta = 1 / totalDistance[i][0] # Delta Pheromne
            for j in range(len(cityList)):
                pheromne[int(routes[i, j]) - 1, int(routes[i, j+1]) - 1] += delta
                pheromne[int(routes[i, j + 1]) - 1, int(routes[i, j]) - 1] += delta

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
    log.printToLog(f"The best routes: {'-'.join(map(str, map(int, bestRoute)))} | Total Distance = {bestDistance[0]:.4f}")
    log.printToLog(f"total generation: {nGeneration}")
    return bestDistances[-1], bestDistances, nGeneration, timeExecution