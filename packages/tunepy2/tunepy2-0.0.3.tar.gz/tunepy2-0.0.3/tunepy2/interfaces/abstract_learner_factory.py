from abc import ABC, abstractmethod
from typing import Tuple

from tunepy2.interfaces import AbstractLearner


class AbstractLearnerFactory(ABC):
    """
    The common interface that tunepy2 expects from all model builders.
    """

    @abstractmethod
    def build(self, bitstring: Tuple) -> AbstractLearner:
        """
        Builds a new model object with hyperparameters derived from the provided bitstring

        :param bitstring: a bitstring representing hyperparameters for this model
        :return: a new, untrained learner
        """
        pass
