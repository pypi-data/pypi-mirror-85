from typing import List

from tunepy2.interfaces import AbstractOptimizer, AbstractGenomeFactory, AbstractConvergenceCriterion
from tunepy2 import get_best_genome, Genome


class BasicGeneticOptimizer(AbstractOptimizer):
    """
    Optimizes fitness using successive refinements of a random population of solutions.
    """

    def __init__(
            self,
            initial_population: List[Genome],
            genome_factory: AbstractGenomeFactory,
            convergence_criterion: AbstractConvergenceCriterion):
        """
        Creates a new BasicGeneticOptimizer.

        :param initial_population: initial seed of Genome objects
        :param genome_factory: creates new Genome objects
        :param convergence_criterion: will declare convergence once criterion is satisfied
        """
        self._population = initial_population
        self._genome_factory = genome_factory
        self._convergence_criterion = convergence_criterion
        self._max_fitness = float('-inf')
        self._best_genome = None
        self._converged = False

    def next(self):
        """
        Performs the next iteration of optimization.

        """
        old_population = self._population

        self._population = []

        for index in range(len(old_population)):
            new_genome = self._genome_factory.build(old_population)
            self._population.append(new_genome)
            new_genome.run()
            if new_genome.fitness > self._max_fitness:
                self._best_genome = new_genome
                self._max_fitness = self._best_genome.fitness

        self._converged = self._convergence_criterion.converged(get_best_genome(old_population), self.best_genome)

    @property
    def converged(self) -> bool:
        """
        Whether or not this algorithm has converged

        :return: true when this algorithm has converged or false if not
        """
        return self._converged

    @property
    def best_genome(self) -> Genome:
        """
        The best genome so far

        :return: a Genome instance
        """
        if self._best_genome is None:
            self._best_genome = get_best_genome(self._population)
        return self._best_genome
