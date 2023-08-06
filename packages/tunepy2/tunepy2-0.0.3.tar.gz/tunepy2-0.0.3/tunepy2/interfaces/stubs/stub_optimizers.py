from tunepy2.interfaces import AbstractOptimizer


class ConvergedOptimizer(AbstractOptimizer):
    """
    Always appears to have converged.
    """

    @property
    def best_genome(self):
        return None

    @property
    def converged(self):
        return True

    def next(self):
        pass
