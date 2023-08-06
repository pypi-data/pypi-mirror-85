from typing import Tuple, Callable

from tunepy2 import Genome
from tunepy2.interfaces import AbstractOptimizer
from tunepy2.optimizers.meta import BasicRestartOptimizer
from tunepy2.optimizers import BasicAnnealingOptimizer, BasicOptimizer, BasicGeneticOptimizer
from tunepy2.convergence import Iterations, ConsecutiveNonImprovement, ExponentialAnnealingSchedule
from tunepy2.optimizers.builders import BasicOptimizerBuilder
from tunepy2.genome_factory import RandomGenomeFactory, \
    RandomNeighborGenomeFactory, \
    SinglePointCrossoverGenomeFactory
from tunepy2.random import NumpyRNG
from tunepy2.comparison import RouletteWheelComparer


def new_random_restart_hill_climber(
        dimensions: Tuple,
        restarts: int,
        convergence_iterations: int,
        epsilon: float,
        fitness_func: Callable[..., float],
        *args,
        **kwargs) -> AbstractOptimizer:
    """
    Builds a new optimizer that generates and evaluates a candidate, finds a neighbor of this candidate,
    and determines if the neighbor is more suitable than the original candidate. It performs this optimization a set
    number of times.

    :param dimensions: dimension of bitstrings passed into fitness_func
    :param restarts: number of times to run the optimization
    :param convergence_iterations: number candidates to evaluate without improvement before declaring convergence
    :param epsilon: minimum required improvement between candidates to continue
    :param fitness_func: function to optimize (accepts a bitstring)
    :param args: will be passed into fitness_func
    :param kwargs: will be passed into fitness_func
    :return: a new optimizer
    """
    random = NumpyRNG()

    random_genome_factory = \
        RandomGenomeFactory(
            dimensions,
            random,
            fitness_func,
            *args,
            **kwargs)

    neighbor_genome_factory = \
        RandomNeighborGenomeFactory(
            dimensions,
            random,
            1,
            fitness_func,
            *args,
            **kwargs)

    restart_convergence = Iterations(restarts)

    single_optimizer_convergence = ConsecutiveNonImprovement(convergence_iterations, epsilon)

    optimizer_builder = \
        BasicOptimizerBuilder(
            dimensions,
            random,
            neighbor_genome_factory,
            single_optimizer_convergence,
            fitness_func,
            *args,
            **kwargs)

    return BasicRestartOptimizer(
        optimizer_builder,
        random_genome_factory,
        1,
        restart_convergence)


def new_simulated_annealer(
        dimensions: Tuple,
        max_neighbor_distance: int,
        initial_temperature: float,
        minimum_temperature: float,
        degradation_multiplier: float,
        fitness_func: Callable[..., float],
        *args,
        **kwargs) -> AbstractOptimizer:
    """
    Creates a new optimizer that optimizes by simulated annealing using a default temperature schedule.

    :param dimensions: dimension of bitstrings passed into fitness_func
    :param max_neighbor_distance: Manhattan distance allowed between neighbors
    :param initial_temperature: starting temperature
    :param minimum_temperature: minimum temperature before convergence
    :param degradation_multiplier: temperature will be multiplied by this every iteration
    :param fitness_func: function to optimize (accepts a bitstring)
    :param args: will be passed into fitness_func
    :param kwargs: will be passed into fitness_func
    :return: a new optimizer
    """
    random = NumpyRNG()

    neighbor_genome_factory = \
        RandomNeighborGenomeFactory(
            dimensions,
            random,
            max_neighbor_distance,
            fitness_func,
            *args,
            **kwargs)

    annealing_schedule = \
        ExponentialAnnealingSchedule(
            initial_temperature,
            minimum_temperature,
            degradation_multiplier)

    initial_candidate = \
        Genome.new_default_genome(
            dimensions,
            fitness_func,
            *args,
            **kwargs)

    initial_candidate.run()

    return BasicAnnealingOptimizer(
        initial_candidate,
        neighbor_genome_factory,
        annealing_schedule,
        random)


def new_hill_climber(
        dimensions: Tuple,
        convergence_iterations: int,
        epsilon: float,
        fitness_func: Callable[..., float],
        *args,
        **kwargs) -> AbstractOptimizer:
    """
    Builds a new optimizer that generates and evaluates a candidate, finds a neighbor of this candidate,
    and determines if the neighbor is more suitable than the original candidate.

    :param dimensions: dimension of bitstrings passed into fitness_func
    :param convergence_iterations: number candidates to evaluate without improvement before declaring convergence
    :param epsilon: minimum required improvement between candidates to continue
    :param fitness_func: function to optimize (accepts a bitstring)
    :param args: will be passed into fitness_func
    :param kwargs: will be passed into fitness_func
    :return: a new optimizer
    """
    random = NumpyRNG()

    neighbor_genome_factory = \
        RandomNeighborGenomeFactory(
            dimensions,
            random,
            1,
            fitness_func,
            *args,
            **kwargs)

    initial_candidate = \
        Genome.new_default_genome(
            dimensions,
            fitness_func,
            *args,
            **kwargs)

    initial_candidate.run()

    convergence_criterion = ConsecutiveNonImprovement(convergence_iterations, epsilon)

    return BasicOptimizer(
        initial_candidate,
        neighbor_genome_factory,
        convergence_criterion)


def new_genetic_optimizer(
        dimensions: Tuple,
        population_size: int,
        mutation_rate: float,
        convergence_iterations: int,
        epsilon: float,
        fitness_func: Callable[..., float],
        *args,
        **kwargs) -> AbstractOptimizer:
    """
    Builds a new optimizer that evaluates a population's fitness, probabilistically chooses the best candidates,
    and constructs a new population from the old. It continues this until the best candidate from the population is
    no longer improving between generations.

    :param dimensions:
    :param population_size: population size of each generation
    :param mutation_rate: probability of a single candidate mutating
    :param convergence_iterations: number candidates to evaluate without improvement before declaring convergence
    :param epsilon: minimum required improvement between candidates to continue
    :param fitness_func: function to optimize (accepts a bitstring)
    :param args: will be passed into fitness_func
    :param kwargs: will be passed into fitness_func
    :return: a new optimizer
    """
    random = NumpyRNG()

    comparer = RouletteWheelComparer(random)

    genome_factory = \
        SinglePointCrossoverGenomeFactory(
            dimensions,
            random,
            mutation_rate,
            comparer,
            fitness_func,
            *args,
            **kwargs)

    initial_population_genome_factory = \
        RandomGenomeFactory(
            dimensions,
            random,
            fitness_func,
            *args,
            **kwargs)

    convergence_criterion = ConsecutiveNonImprovement(convergence_iterations, epsilon)

    initial_population = []

    for _ in range(population_size):
        new_genome = initial_population_genome_factory.build([])
        new_genome.run()
        initial_population.append(new_genome)

    return BasicGeneticOptimizer(
        initial_population,
        genome_factory,
        convergence_criterion)
