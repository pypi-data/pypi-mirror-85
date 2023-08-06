from typing import Tuple, Callable
from tunepy2 import Genome, InitialPopulationUndefinedException
from tunepy2.interfaces import AbstractOptimizerBuilder, AbstractRandomNumberGenerator, AbstractGenomeFactory, \
    AbstractAnnealingSchedule, AbstractOptimizer
from tunepy2.optimizers import BasicAnnealingOptimizer


class BasicAnnealerOptimizerBuilder(AbstractOptimizerBuilder):
    """
    Builds new instances of BasicAnnealerOptimizer.
    """
    def __init__(
            self,
            dimensions: Tuple,
            rng: AbstractRandomNumberGenerator,
            new_candidate_genome_factory: AbstractGenomeFactory,
            annealing_schedule: AbstractAnnealingSchedule,
            fitness_func: Callable[..., float],
            *args,
            **kwargs):
        """
        Creates a new BasicAnnealerOptimizerBuilder.

        :param dimensions: dimensions of bitstring
        :param rng: a random number generator
        :param new_candidate_genome_factory: factory for building new Genome objects
        :param annealing_schedule: temperature schedule used for the simulated annealing process
        :param fitness_func: fitness function passed into new Genome objects
        :param args: will be passed into fitness_func
        :param kwargs: will be passed into fitness_func
        """
        self._dimensions = dimensions
        self._rng = rng
        self._fitness_func = fitness_func
        self._new_candidate_genome_factory = new_candidate_genome_factory
        self._annealing_schedule = annealing_schedule
        self._args = args
        self._kwargs = kwargs
        self._population = []

    def add_to_initial_population_from_factory(
            self,
            genome_factory: AbstractGenomeFactory,
            n: int) -> AbstractOptimizerBuilder:
        """
        Adds a given number of Genomes to the initial population of this optimizer from a factory

        :param genome_factory: the factory that will generate the Genome
        :param n: number of instances to add
        :return: self
        """
        base_genome = Genome.new_default_genome(genome_factory.dimensions,
                                                self._fitness_func,
                                                *self._args,
                                                **self._kwargs)
        self._population += [genome_factory.build([base_genome]) for _ in range(n)]
        return self

    def add_to_initial_population(self, genome: Genome) -> AbstractOptimizerBuilder:
        """
        Adds a single Genome instance to the initial population of this optimizer

        :param genome: instance to add
        :return: self
        """
        self._population.append(genome)
        return self

    def build(self) -> AbstractOptimizer:
        """
        Constructs a new optimizer

        :return: a new optimizer
        """
        for genome in self._population:
            genome.run()

        if len(self._population) < 1:
            raise InitialPopulationUndefinedException

        initial_candidate = self._population[self._rng.random_int(0, len(self._population))]

        new_optimizer = BasicAnnealingOptimizer(initial_candidate,
                                                self._new_candidate_genome_factory,
                                                self._annealing_schedule,
                                                self._rng)

        return new_optimizer

    def clear(self) -> AbstractOptimizerBuilder:
        """
        Clears the initial population of this builder

        :return: self
        """
        self._population = []
        return self
