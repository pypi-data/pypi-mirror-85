from tunepy2 import Genome
from tunepy2.interfaces import AbstractOptimizer, AbstractGenomeFactory, AbstractAnnealingSchedule, \
    AbstractRandomNumberGenerator
from math import exp


class BasicAnnealingOptimizer(AbstractOptimizer):
    """
    Performs a randomized optimization of by simulated annealing.
    """

    def __init__(
            self,
            initial_candidate: Genome,
            genome_factory: AbstractGenomeFactory,
            annealing_schedule: AbstractAnnealingSchedule,
            rng: AbstractRandomNumberGenerator):
        """
        Creates a new BasicAnnealingOptimizer.

        :param initial_candidate: seed Genome object
        :param genome_factory: builds new Genome objects
        :param annealing_schedule: temperature schedule for simulated annealing
        :param rng: a random number generator
        """
        self._candidate = initial_candidate
        self._genome_factory = genome_factory
        self._annealing_schedule = annealing_schedule
        self._rng = rng
        self._max_fitness = float('-inf')
        self._best_genome = initial_candidate
        self._converged = False

    def next(self):
        """
        Performs the next iteration of optimization.

        """
        old_candidate = self._candidate
        new_candidate = self._genome_factory.build([old_candidate])
        new_candidate.run()

        if new_candidate.fitness > old_candidate.fitness:
            self._candidate = new_candidate
        else:
            acceptance_probability = exp((new_candidate.fitness - old_candidate.fitness) / self.temperature)
            if self._rng.random() < acceptance_probability:
                self._candidate = new_candidate

        if self._candidate.fitness > self._max_fitness:
            self._best_genome = self._candidate
            self._max_fitness = self._candidate.fitness

        self._converged = self._annealing_schedule.converged(old_candidate, self._candidate)

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
        return self._best_genome

    @property
    def temperature(self) -> float:
        """
        The current temperature of the BasicAnnealingOptimizer

        :return: the current temperature
        """
        return self._annealing_schedule.temperature
