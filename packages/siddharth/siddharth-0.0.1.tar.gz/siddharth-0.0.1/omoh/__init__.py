import random

class Omoh:

    species = ["paris", "sydney", "indore", "hyderabad"]

    def returnSpecies(self) :
        return self.species[random.randint(0,3)]
