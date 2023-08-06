from tunepy2.interfaces import AbstractConvergenceCriterion, AbstractAnnealingSchedule


class PassThroughConvergenceCriterion(AbstractConvergenceCriterion):
    """
    Returns the value passed in during instantiation.
    """

    def converged(self, old_candidate, new_candidate):
        return self._return_value

    def __init__(self, return_value):
        self._return_value = return_value


class PassThroughAnnealingSchedule(AbstractAnnealingSchedule):
    @property
    def temperature(self):
        return self._temperature

    def converged(self, old_candidate, new_candidate):
        return self._converged_value

    def __init__(self, temperature_value, converged_value):
        self._temperature = temperature_value
        self._converged_value = converged_value
