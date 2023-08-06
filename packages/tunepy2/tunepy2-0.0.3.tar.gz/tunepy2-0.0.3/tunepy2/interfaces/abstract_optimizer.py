from abc import ABC, abstractmethod

from tunepy2 import Genome


class AbstractOptimizer(ABC):
    """
    The common interface for that tunepy2 expects from all optimizing algorithms.
    """

    @abstractmethod
    def next(self):
        """
        Performs the next iteration of optimization.

        """
        pass

    @property
    @abstractmethod
    def converged(self) -> bool:
        """
        Whether or not this algorithm has converged

        :return: true when this algorithm has converged or false if not
        """
        pass

    @property
    @abstractmethod
    def best_genome(self) -> Genome:
        """
        The best genome so far

        :return: a Genome instance
        """
        pass
