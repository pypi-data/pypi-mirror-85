from tunepy2.interfaces import AbstractValidator


class PassThroughValidator(AbstractValidator):
    """
    A validator that trains one model on all of the provided data and returns its fitness score.
    """

    def validate(self, x, y, model):
        """
        Trains a single model, evaluates on the training set, and returns a fitness score.
        :param x: Array-like dataset features.
        :param y: Array-like dataset labels.
        :param model: An untrained model of a class than implements AbstractLearner.
        :return:
        """

        model.fit(x, y)
        model.evaluate(x)
        return model.fitness
