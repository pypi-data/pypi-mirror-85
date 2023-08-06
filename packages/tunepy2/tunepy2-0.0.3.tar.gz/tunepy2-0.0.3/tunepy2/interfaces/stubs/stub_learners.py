from tunepy2.interfaces import AbstractLearner


class ConstantFitnessLearner(AbstractLearner):
    """
    A learner with a fitness defined on construction.
    """

    def __init__(self, fitness):
        self._fitness = fitness

    def fit(self, x_train, y_train):
        pass

    def evaluate(self, x_test, y_test):
        return self.fitness

    @property
    def fitness(self):
        return self._fitness
