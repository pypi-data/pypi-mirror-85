from typing import Tuple

from tunepy2.interfaces import AbstractLearner
from sklearn.neural_network import MLPRegressor


class SklearnMlpRegressorLearner(AbstractLearner):
    """
    Wraps Sklearn MLPRegressor for hyperparameter search.
    """
    def __init__(
            self,
            *args,
            **kwargs):
        """
        Creates a new SklearnMlpRegressorLearner.

        :param args: will be passed into MLPRegressor during construction
        :param kwargs: will be passed into MLPRegressor during construction
        """
        self._learner = MLPRegressor(*args, **kwargs)
        self._fitness = float("-inf")

    def fit(self, x_train, y_train):
        """
        Trains the model on a labeled dataset

        :param x_train: table of features
        :param y_train: vector of labels
        """
        self._learner.fit(x_train, y_train)

    def evaluate(self, x_test: Tuple, y_test: Tuple) -> float:
        """
        Returns a fitness score after predicting labels on a dataset

        :param x_test: table of features.
        :param y_test: vector of labels for fitness evaluation.
        :return: A fitness score
        """
        self._fitness = self._learner.score(x_test, y_test)
        return self._fitness

    @property
    def fitness(self) -> float:
        """
        The fitness score of this machine learning model

        :return: The fitness score of this machine learning model
        """
        return self._fitness
