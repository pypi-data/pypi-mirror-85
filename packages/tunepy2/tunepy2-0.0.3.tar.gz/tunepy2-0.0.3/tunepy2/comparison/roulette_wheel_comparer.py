from typing import List

from tunepy2 import Genome
from tunepy2.interfaces import AbstractGenomeComparer, AbstractRandomNumberGenerator, AbstractLearner
import numpy as np


class RouletteWheelComparer(AbstractGenomeComparer):
    """ Performs a fitness proportionate random model selection. The underlying implementation uses the stochastic
    acceptance method for producing a result in nearly constant time. This is a common method for selecting
    breeding pairs for a genetic algorithm.
    """

    def __init__(self, random_number_generator: AbstractRandomNumberGenerator):
        """ Constructs a new RouletteWheelComparer

        :param random_number_generator: a random number generator
        """
        self._rng = random_number_generator
        self._hash_models = 0
        self._all_fitness = None
        self._max_fitness = -float('inf')

    def compare(self, genomes: List[Genome]) -> Genome:
        """ Compares a list of Genomes and returns a single Genome

        :param genomes: list of Genome objects to compare
        :return: Genome. the result of comparing all genomes
        """

        self.extract_fitness_from_genomes(genomes)

        while True:
            chosen_genome = genomes[self._rng.random_int(0, len(genomes))]
            acceptance_probability = chosen_genome.fitness / self._max_fitness
            if acceptance_probability > self._rng.random():
                return chosen_genome

    def extract_fitness_from_genomes(self, genomes: List[Genome]) -> None:
        new_hash_models = hash(tuple(genomes))

        self._hash_models = new_hash_models
        self._all_fitness = np.zeros(shape=(len(genomes),))

        for index in range(len(genomes)):
            self._all_fitness[index] = genomes[index].fitness

        self._max_fitness = np.max(self._all_fitness)
