from tunepy2 import Genome
from tunepy2.interfaces import AbstractOptimizer, AbstractOptimizerBuilder, AbstractGenomeFactory, \
    AbstractConvergenceCriterion


class BasicRestartOptimizer(AbstractOptimizer):
    """
    An optimizer that creates other optimizers, tests them to convergence, and repeats until its own convergence
    criterion is met.
    """
    def __init__(
            self,
            optimizer_builder: AbstractOptimizerBuilder,
            genome_factory: AbstractGenomeFactory,
            population_size: int,
            convergence_criterion: AbstractConvergenceCriterion):
        """
        Creates a new BasicRestartOptimizer.

        :param optimizer_builder: builds new optimizers for each iteration of this optimizer
        :param genome_factory: creates Genome objects
        :param population_size: population size for each underlying optimizer
        :param convergence_criterion: convergence criterion used for evaluation of this optimizer
        """
        self._optimizer_builder = optimizer_builder
        self._genome_factory = genome_factory
        self._population_size = population_size
        self._convergence_criterion = convergence_criterion
        self._max_fitness = float('-inf')
        self._converged = False
        self._best_genome = None

    def next(self):
        """
        Performs the next iteration of optimization.

        """
        new_optimizer = self._optimizer_builder\
            .clear()\
            .add_to_initial_population_from_factory(self._genome_factory, self._population_size)\
            .build()

        while not new_optimizer.converged:
            new_optimizer.next()

        self._converged = self._convergence_criterion.converged(self.best_genome, new_optimizer.best_genome)

        if new_optimizer.best_genome.fitness > self._max_fitness:
            self._max_fitness = new_optimizer.best_genome.fitness
            self._best_genome = new_optimizer.best_genome

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
