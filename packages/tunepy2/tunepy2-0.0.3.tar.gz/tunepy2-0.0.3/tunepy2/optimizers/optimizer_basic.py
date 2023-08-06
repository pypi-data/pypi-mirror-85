from tunepy2 import Genome
from tunepy2.interfaces import AbstractOptimizer, AbstractGenomeFactory, AbstractConvergenceCriterion


class BasicOptimizer(AbstractOptimizer):
    """
    A very simple optimizer that builds new Genomes until convergence is satisfied.
    """
    def __init__(
            self,
            initial_candidate: Genome,
            genome_factory: AbstractGenomeFactory,
            convergence_criterion: AbstractConvergenceCriterion):
        """
        Creates a new BasicOptimizer.

        :param initial_candidate: seed Genome object
        :param genome_factory: creates new Genome objects
        :param convergence_criterion: will declare convergence once criterion is satisfied
        """
        self._candidate = initial_candidate
        self._genome_factory = genome_factory
        self._convergence_criterion = convergence_criterion
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

        self._converged = self._convergence_criterion.converged(old_candidate, new_candidate)

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
        return self._candidate
