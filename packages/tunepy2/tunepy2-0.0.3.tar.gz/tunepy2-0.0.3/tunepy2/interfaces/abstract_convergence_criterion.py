from abc import ABC, abstractmethod

from tunepy2 import Genome


class AbstractConvergenceCriterion(ABC):
    """Interface for algorithms that declare convergence of an optimizer"""

    @abstractmethod
    def converged(self, old_candidate: Genome, new_candidate: Genome) -> bool:
        """
        Determines if convergence has been reached based on current and prior Genome objects

        :param old_candidate: Genome object from prior iteration
        :param new_candidate: Genome object from current iteration
        :return: true if converged
        """
        pass


class AbstractAnnealingSchedule(AbstractConvergenceCriterion):
    """Interface for defining annealing schedules"""

    @property
    @abstractmethod
    def temperature(self) -> float:
        """ The current temperature of the annealing schedule

        :return: float value of current temperature
        """
        pass
