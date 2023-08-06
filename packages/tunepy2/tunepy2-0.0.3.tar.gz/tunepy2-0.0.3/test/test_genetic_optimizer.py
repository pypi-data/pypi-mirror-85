import unittest
from tunepy2.optimizers import BasicGeneticOptimizer
from tunepy2.interfaces.stubs import PassThroughConvergenceCriterion, PassThroughGenomeFactory
from tunepy2.internal import Genome


class TestGeneticOptimizer(unittest.TestCase):
    def test_next_generation_improvement(self):
        def fitness_func_zero(bitstring):
            return 0

        def fitness_func_one(bitstring):
            return 1

        initial_population = [Genome(fitness_func_zero, (0,))]
        for genome in initial_population:
            genome.run()

        convergence_criterion = PassThroughConvergenceCriterion(True)
        genome_builder = PassThroughGenomeFactory(Genome(fitness_func_one, (1,)))
        optimizer = BasicGeneticOptimizer(initial_population, genome_builder, convergence_criterion)

        optimizer.next()

        self.assertEqual(1, optimizer.best_genome.fitness)

    def test_convergence(self):
        def fitness_func_zero(bitstring):
            return 0

        initial_population = [Genome(fitness_func_zero, (0,))]
        for genome in initial_population:
            genome.run()

        convergence_criterion = PassThroughConvergenceCriterion(True)
        genome_builder = PassThroughGenomeFactory(Genome(fitness_func_zero, (1,)))
        optimizer = BasicGeneticOptimizer(initial_population, genome_builder, convergence_criterion)

        self.assertFalse(optimizer.converged)
        optimizer.next()
        self.assertTrue(optimizer.converged)


if __name__ == '__main__':
    unittest.main()
