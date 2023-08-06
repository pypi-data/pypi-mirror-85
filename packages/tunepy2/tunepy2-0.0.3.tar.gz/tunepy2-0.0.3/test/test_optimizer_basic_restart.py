import unittest

from tunepy2.optimizers.meta import BasicRestartOptimizer
from tunepy2.optimizers.builders import BasicOptimizerBuilder
from tunepy2.interfaces.stubs import PassThroughGenomeFactory, PassThroughConvergenceCriterion
from tunepy2.random import NumpyRNG
from tunepy2 import Genome


class TestOptimizerBasicRestart(unittest.TestCase):
    def test_convergence(self):
        def fitness_func(bitstring):
            return 69.0

        new_population_genome_factory = PassThroughGenomeFactory(
            Genome.new_default_genome(
                (5,),
                fitness_func
            )
        )
        convergence_criterion = PassThroughConvergenceCriterion(True)
        optimizer_builder = BasicOptimizerBuilder(
            (5,),
            NumpyRNG(),
            new_population_genome_factory,
            convergence_criterion,
            fitness_func
        )

        meta_optimizer = BasicRestartOptimizer(
            optimizer_builder,
            new_population_genome_factory,
            10,
            convergence_criterion
        )

        meta_optimizer.next()
        self.assertAlmostEqual(meta_optimizer.best_genome.fitness, 69.0)
        self.assertTrue(meta_optimizer.converged)


if __name__ == '__main__':
    unittest.main()
