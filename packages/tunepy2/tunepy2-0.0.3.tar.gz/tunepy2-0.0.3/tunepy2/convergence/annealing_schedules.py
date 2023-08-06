from tunepy2 import Genome
from tunepy2.interfaces import AbstractAnnealingSchedule


class ExponentialAnnealingSchedule(AbstractAnnealingSchedule):
    def __init__(self, initial_temperature: float, minimum_temperature: float, degradation_multiplier: float):
        """ Creates a new ExponentialAnnealingSchedule

        :param initial_temperature: starting temperature
        :param minimum_temperature: minimum possible temperature
        :param degradation_multiplier: temperature multiplier (must be less than 1.0)
        """
        self._temperature = initial_temperature
        self._minimum_temperature = minimum_temperature
        self._degradation_multiplier = degradation_multiplier

    @property
    def temperature(self) -> float:
        """ The current temperature of the annealing schedule

        :return: float value of current temperature
        """
        return self._temperature

    def converged(self, old_candidate: Genome, new_candidate: Genome) -> bool:
        """ Determines if convergence has been reached based on current and prior Genome objects

        :param old_candidate: Genome object from prior iteration
        :param new_candidate: Genome object from current iteration
        :return: true if converged
        """
        return_value = self._temperature < self._minimum_temperature
        self._temperature *= self._degradation_multiplier
        return return_value
