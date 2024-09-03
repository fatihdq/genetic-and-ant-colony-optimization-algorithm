import numpy as np
import matplotlib.pyplot as plt 

from base.city import City
from base.route import Route

def gaAcoAlgorithm(city, genCriteria, nAnts, rho, alpha, beta, initialPheromne, routes, DEBUG=False):
    cityList = []
    for i in range(0, len(city)):
        cityList.append(City(name = city.iloc[i,0],x=city.iloc[i][1],y=city.iloc[i][2]))

    distances = np.zeros((len(cityList), len(cityList)))
    visibility = np.zeros((len(cityList), len(cityList)))

    for row in range(len(cityList)):
        for col in range (len(cityList)):
            distance = cityList[row].distance(cityList[col])
            distances[row, col] = distance
            visibility[row, col] = 1/distance  if distance != 0 else 0

    # Calculate total distance in Genetica algorithm result
    totalDistance = np.zeros((len(routes), 1)) # initiate total distance
    print(f"Genetica Algorithm Result: ")
    for i in range(len(routes)):
        routeStr = ""
        distance = 0
        for j in range(len(routes[i])-1):
            distance += routes[i][j].distance(routes[i][j+1])
            routeStr += " "+str(routes[i][j].name)
        routeStr += " "+str(routes[i][-1].name)
        print(f"Ant {i+1}: [{routeStr}] Distance: {Route(routes[i]).routeDistance()}")
        totalDistance[i] = distance

    # Inisialization Pheromne
    pheromne = initialPheromne * np.ones((len(cityList), len(cityList)))
    # Update pheromne with genetica algorithm result
    pheromne = (1 - rho) * pheromne # Evaporation
    for i in range(len(routes)):
        delta = 1 / totalDistance[i][0] # Delta Pheromne
        for j in range(len(cityList)):
            pheromne[int(routes[i][j].name) - 1, int(routes[i][j+1].name) - 1] += delta
            pheromne[int(routes[i][j + 1].name) - 1, int(routes[i][j].name) - 1] += delta

    print("\nInitial Pheromne")
    print("--------------------------------")
    print("Initail City | Destination City | Pheromne")
    for row in range(len(cityList)):
        for col in range (row+1,len(cityList)):
            print(f"{row + 1}             | {col + 1}               | {pheromne[row, col]:.4f}")
    print("------------------------------------------\n")

    bestRoute = None
    bestDistance = float('inf')
    bestDistances = []

    # ACO Iteration
    sameResult = []
    looping = True
    idx = 0
    while looping:
        if DEBUG or idx == 0:
            print(f"=========================== Iteration {idx+1} ============================")
        antAndDistanceStr = ""

        routes = np.ones((nAnts, len(cityList)+1), dtype=int)
    
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
                    print(f"Ant {i + 1}: {routes[i, :]}")
                    print("---------------------")
                    print("City  | Probability |")
                    for k in range(len(cityList)):
                        print(f"{k + 1}     | {probabilities[k]:.4f}       |")
                    print("---------------------")

                # Choose next city with highest probability
                nextCityIdx = np.argmax(probabilities)
                routes[i, j+1] = nextCityIdx + 1 # Add next city to route

                distance += distances[int(routes[i, j]) - 1, int(routes[i, j+1]) - 1]


            routes[i, -1] = routes[i, 0] # Back to first City
            if DEBUG:
                print(f"Ant {i + 1}: {routes[i, :]}")

            # Calculate last city to first city
            distance += distances[int(routes[i, -2]) - 1, int(routes[i, -1]) - 1]
            totalDistance[i] = distance
            antAndDistanceStr += f"Ant {i+1}: {'-'.join(map(str, map(int, routes[i, :])))} | Distance = {totalDistance[i, 0]:.4f}\n"
            if DEBUG:
                print("\n====================\n")

        if DEBUG:
            print(f"Iteration {idx+1} Result: ")
            print(antAndDistanceStr)


        # Search the best routes
        distanceMinIdx = np.argmin(totalDistance)
        distanceMin = totalDistance[distanceMinIdx]
        if distanceMin < bestDistance:
            bestDistance = distanceMin
            bestRoute = routes[distanceMinIdx, :]

        bestDistances.append(bestDistance)

        if len(sameResult) == 0:
            sameResult.append(bestDistance)
        else:
            if sameResult[-1] == bestDistance:
                sameResult.append(bestDistance)
            else:
                sameResult = []
        
        if len(sameResult) == genCriteria:
            looping = False

        # Update pheromne
        pheromne = (1 - rho) * pheromne # Evaporation
        for i in range(nAnts):
            delta = 1 / totalDistance[i][0] # Delta Pheromne
            for j in range(len(cityList)):
                pheromne[int(routes[i, j]) - 1, int(routes[i, j+1]) - 1] += delta
                pheromne[int(routes[i, j + 1]) - 1, int(routes[i, j]) - 1] += delta
        
        if DEBUG == False and looping == False:
            print(f"=========================== Iteration {idx+1} ============================")

        if DEBUG or looping == False or idx == 0 :
            print("Update Pheromne")
            print("--------------------------------")
            print("Initail City | Destination City | New Pheromne")
        for i in range(len(cityList)):
            for j in range(i+1, len(cityList)):
                pheromneValue = pheromne[i, j]
                if DEBUG or looping == False or idx == 0:
                    print(f"{i + 1}             | {j + 1}               | {pheromneValue:.4f}")
        if DEBUG or looping == False or idx == 0:
            print("------------------------------------------\n")
        
        idx += 1

    nGeneration = idx
    print(f"The best routes: {'-'.join(map(str, map(int, bestRoute)))} | Total Distance = {bestDistance[0]:.4f}")
    print(f"total generation: {nGeneration}")
    return bestDistances[-1], bestDistances, nGeneration