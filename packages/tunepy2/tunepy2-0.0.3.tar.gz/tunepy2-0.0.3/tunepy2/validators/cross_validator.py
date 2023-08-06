from typing import Tuple

from tunepy2.interfaces import AbstractValidator, AbstractLearner
from tunepy2.internal import *
import numpy as np
from copy import deepcopy


class CrossValidator(AbstractValidator):
    """
    Trains a set number of models on subsets of the provided data and returns the average fitness
    of the trained models.
    """

    def __init__(self, bins: int):
        """
        Creates a new CrossValidator.

        :param bins: number of bins (must be at least 2)
        """
        self._bins = bins
        self._feature_bins_train = []
        self._feature_bins_test = []
        self._label_bins_train = []
        self._label_bins_test = []

    def validate(self, x, y, model: AbstractLearner) -> float:
        """
        Creates a fitness score for the provided model and data

        :param x: array-like dataset features
        :param y: array-like dataset labels
        :param model: untrained learner
        :return: a fitness score
        """
        if self._bins < 2:
            raise CrossValidatorBinException

        if len(x) != len(y):
            raise DimensionsMismatchException

        self.build_test_bins(x, y)
        self.build_train_bins(x, y)

        total_fitness = 0.0

        for index in range(self._bins):
            model_copy = deepcopy(model)
            model_copy.fit(self._feature_bins_train[index], self._label_bins_train[index])
            model_copy.evaluate(self._label_bins_test[index], self._label_bins_train[index])
            total_fitness += model_copy.fitness
        return float(total_fitness / self._bins)

    def build_test_bins(self, x, y):
        if len(x) != len(y):
            raise DimensionsMismatchException

        total_rows = len(y)
        extra_rows = total_rows % self._bins
        bin_size = int((total_rows - extra_rows) / self._bins)

        self._feature_bins_test = [None for _ in range(self._bins)]
        self._label_bins_test = [None for _ in range(self._bins)]

        for index in range(self._bins):
            start_slice = index * bin_size
            end_slice = (index + 1) * bin_size
            if index == self._bins - 1:
                self._feature_bins_test[index] = x[start_slice:]
                self._label_bins_test[index] = y[start_slice:]
            else:
                self._feature_bins_test[index] = x[start_slice:end_slice]
                self._label_bins_test[index] = y[start_slice:end_slice]

    def build_train_bins(self, x, y):
        if len(x) != len(y):
            raise DimensionsMismatchException

        total_rows = len(y)
        extra_rows = total_rows % self._bins
        bin_size = int((total_rows - extra_rows) / self._bins)

        self._feature_bins_train = [None for _ in range(self._bins)]
        self._label_bins_train = [None for _ in range(self._bins)]

        for index in range(self._bins):
            start_slice = index * bin_size
            end_slice = (index + 1) * bin_size
            if index == 0:
                self._feature_bins_train[index] = x[end_slice:]
                self._label_bins_train[index] = y[end_slice:]
            elif index == self._bins - 1:
                self._feature_bins_train[index] = x[:start_slice]
                self._label_bins_train[index] = y[:start_slice]
            else:
                self._feature_bins_train[index] = np.concatenate((x[:start_slice], x[end_slice:]), axis=0)
                self._label_bins_train[index] = np.concatenate((y[:start_slice], y[end_slice:]), axis=0)

    @property
    def bins(self):
        return self._bins

    @property
    def training_data_features(self):
        return self._feature_bins_train

    @property
    def training_data_labels(self):
        return self._label_bins_train

    @property
    def test_data_features(self):
        return self._feature_bins_test

    @property
    def test_data_labels(self):
        return self._label_bins_test



