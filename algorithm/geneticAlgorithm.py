import random

from base.route import Route

def createRoute(cityList):
    #Randomize city based on city in dataset to assign into route
    route = random.sample(cityList, len(cityList))
    return route

def initialPopulation(popSize, cityList):
    population = []
    # Create population based on population size
    for i in range(0, popSize):
      route = createRoute(cityList)
      while route in population:
        route = createRoute(cityList)
      population.append(createRoute(cityList))
    return population

def rankRoutes(population):
    fitnessResults = []
    rankRoute = {}

    #Determine fitness each individual in population
    for i in range(0, len(population)):
        fitnessResults.append(Route(population[i]).routeFitness())

    #Sorting based on fitness value
    sortedFitness = sorted(fitnessResults, reverse=True)
    for i in range(0, len(sortedFitness)):
        for j in range(0, len(population)):
            if sortedFitness[i] == Route(population[j]).routeFitness():
                rankRoute[i] = population[j]

    return rankRoute

def selection(population, DEBUG=False):
    selection = []
    #Take first 2  the best individuals
    for i in range(0,2):
        selection.append(population[i])
        if DEBUG:
            print("seleksi ke-" + str(i+1) + " " + str(Route(selection[i]).printCity()) + "\n" +
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

def crossover(parent1, parent2, tab, DEBUG=False):
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
        print("stargene = "+str(startGene+1)+", endGene = "+str(endGene+1))

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

def mutate(individual,DEBUG=False):
    #randomizes the gene number to be exchanged
    swapped = random.randint(1, len(individual)-1)
    swapWith = random.randint(1, len(individual)-1)
    #swapped and swapWith cannot have the same value
    while swapped == swapWith:
        swapWith = random.randint(1, len(individual)-1)

    city1 = individual[swapped]
    city2 = individual[swapWith]

    if DEBUG:
        print("swapped = "+str(swapped+1) + " , swap with = " + str(swapWith+1))

    #hasil mutasi
    individual[swapped] = city2
    individual[swapWith] = city1
    return individual

def updateGeneration(population,popsize,mutate,DEBUG=False):
    generasibaru =[]
    #combining populations with mutation results to create a new generation
    for i in range(0,popsize):
        generasibaru.append(population[i])

    #replace the individual with the smallest fitness (last index) with the mutation result if the mutation result is greater
    if Route(mutate).routeFitness() >= Route(generasibaru[-1]).routeFitness():
      generasibaru[popsize-1] =mutate
    if DEBUG:
        for i in range(0,popsize):
            print("Generasi baru ke-" + str(i+1) + " " + str(Route(generasibaru[i]).printCity()) +
                " Jarak = " + str(Route(generasibaru[i]).routeDistance()) + " Fitness = " + str(
                Route(generasibaru[i]).routeFitness()))

    return generasibaru

def geneticAlgorithm(population, popSize, generations, DEBUG=False, imageFilename='./images/ga_result.png'):
    tabulistResult = []
    finalPopulation = []
    pop = []

    # Create Population
    populasi = initialPopulation(popSize, population)

    # Sort each individual in population based on ranking
    rankPopulasi = rankRoutes(populasi)
    for i in range(0, popSize):
        pop.append(rankPopulasi[i])

    # Start genetic algorithm with the first generation
    print("=========================== GENERASI KE " + str(1) + "===============================================================>")
    for i in range(0,len(pop)):
        print("populasi ke-" + str(i+1) + " " + str(Route(pop[i]).printCity()) +
              " Jarak = " + str(Route(pop[i]).routeDistance()) + " Fitness = " + str(
            Route(pop[i]).routeFitness()))
    print("==========================================================================================>")

    bestDistance = 9999999999999
    progress =[]
    for i in range(0, generations):
        nextGeneration = []

        #Selection process
        selectionResults = selection(pop, DEBUG)

        #Check Tabulist
        tab, tabulistResult = tabulist(selectionResults, tabulistResult)

        #Crossover if the tabulist true
        crossoverResult = crossover(selectionResults[0], selectionResults[1], tab, DEBUG)
        if DEBUG:
            if tab == False:
                print("Tabulist False")
                print("==========================================================================================>")
                print("hasil crossover = " + str(crossoverResult))
                print("==========================================================================================>")
            elif tab == True:
                print("Tabulist true")
                print("==========================================================================================>")
                print("seleksi 1 = " + str(crossoverResult))
                print("==========================================================================================>")
            print("TABULIST : ", tabulistResult, "\n")

        #Mutate Process
        children = mutate(crossoverResult,DEBUG)
        if DEBUG:
            print("hasil mutasi = " + str(children) + " Jarak = " + str(Route(children).routeDistance()) + " Fitness = " + str(
                Route(children).routeFitness()))
            print("==========================================================================================>")

        #Update Generation
        nextGeneration = updateGeneration(pop, popSize, children, DEBUG)
        poptemp = nextGeneration

        # Sorting new generations based on fitness
        poptemp = rankRoutes(poptemp)
        pop = []
        for j in range(0, popSize):
            pop.append(poptemp[j])

        # Save the best individual in this generation
        tempbestroute = Route(pop[0]).routeDistance()
        progress.append(Route(pop[0]).routeDistance())
        if (bestDistance > tempbestroute):
            bestIndividu = Route(pop[0]).printCity()
            bestDistance = Route(pop[0]).routeDistance()
            bestFitness = Route(pop[0]).routeFitness()

        # Next Generation process
        finalPopulation = pop
        if (DEBUG and i < generations-1) or (i == generations-1): 
            print("\n====================================== GENERASI KE " + str(
                i + 2) + "======================================>")
            for n in range(0, len(pop)):
                print("populasi ke-" + str(n+1) + " " + str(Route(pop[n]).printCity()) +
                    " Jarak = " + str(Route(pop[n]).routeDistance()) + " Fitness = " + str(
                    Route(pop[n]).routeFitness()))
            print("=========================================================================================>")


    print("BEST INDIVIDU = " + str(bestIndividu))
    print("BEST DISTANCE = " + str(bestDistance))
    print("BEST FITNESS = " + str(bestFitness))

    return finalPopulation, bestDistance, progress