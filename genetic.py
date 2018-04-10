import random
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
        print('Thing')
    def calcFitness(self):
        self.fitness = (4 * self.genome[0]**2) - 
        (2 * self.genome[1]**3) + 
        (9 * self.genome[2]**2) - 
        (11 * self.genome[3]**2) + 
        (5 * self.genome[4]**0.5) + 
        (self.genome[5] + self.genome[6])**3 - 
        (5 * self.genome[7]**2) + 
        10 * (self.genome[8] - self.genome[9])**2

    def __str__(self):
        return "(" + ", ".join(str(x) for x in self.genome) + ")"

class Agent:
    population = []

gene = Gene([4, 1, 7, 2, 9, 8, 5, 6, 10, 3])
print (gene)
