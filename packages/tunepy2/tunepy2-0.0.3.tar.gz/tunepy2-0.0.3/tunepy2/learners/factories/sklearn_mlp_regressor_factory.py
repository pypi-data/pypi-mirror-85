from typing import List, Dict, Tuple

from tunepy2 import transform_bitstring_to_layers_tuple
from tunepy2.interfaces import AbstractLearnerFactory, AbstractLearner
from tunepy2.learners import SklearnMlpRegressorLearner


class SklearnMlpRegressorFactory(AbstractLearnerFactory):
    """
    Transforms bitstrings into SklearnMlpRegressorLearner.
    """
    def __init__(
            self,
            *args,
            **kwargs):
        """
        Creates a new SklearnMlpRegressorFactory.

        :param args: will be passed into MLPRegressor
        :param kwargs: will be passed into MLPRegressor
        """
        self._args = args
        self._kwargs = kwargs

    def build(self, bitstring: Tuple) -> AbstractLearner:
        """
        Builds a new model object with hyperparameters derived from the provided bitstring

        :param bitstring: a bitstring representing hyperparameters for this model
        :return: a new, untrained learner
        """
        layers = transform_bitstring_to_layers_tuple(bitstring)
        return SklearnMlpRegressorLearner(layers=layers, *self._args, **self._kwargs)
