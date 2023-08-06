from tunepy2 import Genome
from tunepy2.interfaces import AbstractConvergenceCriterion


class Iterations(AbstractConvergenceCriterion):
    """ Declares convergence after a set number of iterations """

    def __init__(self, n: int):
        """ Creates a new Iterations convergence criterion

        :param n: number of iterations before declaring convergence
        """
        self._n = n
        self._current_iteration = 1

    def converged(self, old_candidate: Genome, new_candidate: Genome) -> bool:
        """ Determines if convergence has been reached based on current and prior Genome objects

        :param old_candidate: Genome object from prior iteration
        :param new_candidate: Genome object from current iteration
        :return: true if converged
        """
        if self._current_iteration >= self._n:
            return True

        self._current_iteration += 1
        return False


class ConsecutiveNonImprovement(AbstractConvergenceCriterion):
    """ Declares convergence after a number of iterations without any improvement in fitness """

    def __init__(self, n: int, epsilon: float):
        """ Creates a new ConsecutiveNonImprovement convergence criterion

        :param n: number of iterations
        :param epsilon: minimum required improvement over n iterations
        """
        self._last_iteration = n - 1
        self._iteration_count = 0
        self._epsilon = epsilon
        self._net_improvement = 0.0

    def converged(self, old_candidate: Genome, new_candidate: Genome) -> bool:
        """ Determines if convergence has been reached based on current and prior Genome objects

        :param old_candidate: Genome object from prior iteration
        :param new_candidate: Genome object from current iteration
        :return: true if converged
        """
        if self._net_improvement < self._epsilon and self._iteration_count == self._last_iteration:
            return True

        old_fitness = old_candidate.fitness
        new_fitness = new_candidate.fitness

        if self._iteration_count == 0:
            self._net_improvement = new_fitness - old_fitness
        else:
            self._net_improvement += new_fitness - old_fitness

        if self._net_improvement < self._epsilon:
            self._iteration_count += 1
        else:
            self._iteration_count = 0

        return False
