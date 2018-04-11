import random
import math
class Gene:
    genome = []
    fitness = 0
    def __init__(self, genome=False):
        # If not given a genome, we randomly generate
        if genome == False:
            self.genome = [1,2,3,4,5,6,7,8,9,10]
            random.shuffle(self.genome)
        else:
            # If given a genome we assign it
            self.genome = genome
        self.calcFitness()

    def calcFitness(self):
        self.fitness = ((4 * self.genome[0]**2) - 
        (2 * self.genome[1]**3) + 
        (9 * self.genome[2]**2) - 
        (11 * self.genome[3]**2) +
        (5 * math.sqrt(self.genome[4])) + 
        ((self.genome[5] + self.genome[6])**3) -
        (5 * self.genome[7]**2) + 
        (10 * (self.genome[8] - self.genome[9])**2))

    def __str__(self):
        return "(" + ", ".join(str(x) for x in self.genome) + ") = " + str(self.fitness)

class Agent:
    population = []
    mutationProb = 0
    crossoverProb = 0
    numGenerations = 0
    minimize = True
    eliteism = False
    def __init__(self, populationSize, mutationProb, crossoverProb, numGenerations, minimize=True, eliteism=False):
        # Setup our passed in values for this run.
        self.mutationProb = mutationProb * .01
        self.crossoverProb = crossoverProb * .01
        self.numGenerations = numGenerations
        self.minimize = minimize
        self.eliteism = eliteism
        
        # Generate starting population
        for _ in range(0, populationSize):
            self.population.append(Gene())
        
        self.sortPopulation()
    
    def sortPopulation(self):
        # Call inline sort with the key being fitness. We reverse if caller requested.
        self.population.sort(key=lambda gene: gene.fitness, reverse=not self.minimize)
    
    def rouletteSelection(self):
        parent1 = None
        parent2 = None
        # Get shift in fitness so everything is either positive or negative depending on minimize or maximize.
        shift = self.population[len(self.population) - 1].fitness
        if self.minimize:
            shift += 1
            shift = -shift
            # for gene in self.population:
            #     if gene.fitness > shift:
            #         shift = -gene.fitness
        else:
            shift -= 1
            shift = -shift
            # for gene in self.population:
            #     if gene.fitness < shift:
            #         shift = -gene.fitness
        # Get total fitness.
        totalFitness = 0
        for gene in self.population:
            totalFitness += (gene.fitness + shift)

        # Get random number
        spin = random.random()

        # Pick gene to use based on fitness
        sumPercent = 0
        parentIndex = 0
        for gene in self.population:
            sumPercent += (gene.fitness + shift) / totalFitness
            if spin < sumPercent:
                parent1 = gene
                parent1.index = parentIndex
                break
            parentIndex += 1
        
        # We need to respin if we get the same parent back
        parent2 = parent1
        while parent1 == parent2:
            # Get random number for parent 2
            spin = random.random()

            # Pick gene to use based on fitness
            sumPercent = 0
            parentIndex = 0
            for gene in self.population:
                sumPercent += (gene.fitness + shift) / totalFitness
                if spin < sumPercent:
                    parent2 = gene
                    parent2.index = parentIndex
                    break
                parentIndex += 1
        return parent1, parent2

    def mate(self, parent1, parent2):
        childGenome1 = []
        childGenome2 = []
        
        # Do we crossover?
        spin = random.random()
        if spin < self.crossoverProb:
            crossoverPoint = random.randint(1, len(parent1.genome))
            childGenome1 += parent1.genome[:crossoverPoint] + parent2.genome[crossoverPoint:]
            childGenome2 += parent2.genome[:crossoverPoint] + parent1.genome[crossoverPoint:]
            self.resolveDuplicates(childGenome1)
            self.resolveDuplicates(childGenome2)
        else:
            childGenome1 = parent1.genome
            childGenome2 = parent2.genome
        
        # Check for mutations in first child
        for i in range(0, len(childGenome1)):
            spin = random.random()
            if spin < self.mutationProb:
                temp = childGenome1[i]
                childGenome1[i] = childGenome1[(i + 1) % len(childGenome1)]
                childGenome1[(i + 1) % len(childGenome1)] = temp
        
        # Check for mutations in second child
        for i in range(0, len(childGenome2)):
            spin = random.random()
            if spin < self.mutationProb:
                temp = childGenome2[i]
                childGenome2[i] = childGenome2[(i + 1) % len(childGenome2)]
                childGenome2[(i + 1) % len(childGenome2)] = temp

        return Gene(childGenome1), Gene(childGenome2)
    
    def resolveDuplicates(self, genome):
        missingGenes = [gene for gene in [1,2,3,4,5,6,7,8,9,10] if gene not in genome]
        for i in range(0, len(genome)):
            if genome.count(genome[i]) > 1:
                genome[i] = missingGenes.pop(0)
        return genome


        
    
    def solve(self):
        # For each generation
        for generationNum in range(0, self.numGenerations):
            # Find parent with roulette selection
            parent1, parent2 = self.rouletteSelection()
            # Mate parents and get children
            child1, child2 = self.mate(parent1, parent2)
            # Remove last two items to fit children
            if self.eliteism:
                # Using eliteism, deleting lowest fitness
                del self.population[-1]
                del self.population[-1]
            else:
                # Delete parents
                del self.population[parent1.index]
                del self.population[parent2.index]
            # Add children to population
            self.population.append(child1)
            self.population.append(child2)
            # Keep population sorted
            self.sortPopulation()
        return self.population[0]

populationSize = int(raw_input('Population Size: '))
mutationProbability = int(raw_input('Mutation Probability (as %): '))
crossoverProbability = int(raw_input('Crossover Probability (as %): '))
numberGenerations = int(raw_input('Number of Generations: '))
minimize = int(raw_input('1 = Minimize function, 2 = Maximize function: ')) == 1
elitism = int(raw_input('1 = Elitism Replacement, 2 = Replace Parents: ')) == 1
agent = Agent(populationSize, mutationProbability, crossoverProbability, numberGenerations, minimize, elitism)
print(agent.solve())