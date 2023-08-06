import unittest
from tunepy2 import new_random_restart_hill_climber, new_simulated_annealer, new_hill_climber, new_genetic_optimizer
from tunepy2.optimizers.meta import BasicRestartOptimizer
from tunepy2.optimizers import BasicAnnealingOptimizer, BasicOptimizer, BasicGeneticOptimizer


class TestPrebuiltOptimizers(unittest.TestCase):
    def test_creates_random_restart_hill_climber(self):
        def fitness_func(bitstring):
            return 69.0

        optimizer = new_random_restart_hill_climber(
            (5,),
            7,
            10,
            1e-5,
            fitness_func)

        self.assertIsInstance(optimizer, BasicRestartOptimizer)
        self.assertFalse(optimizer.converged)

        for _ in range(6):
            optimizer.next()
            self.assertFalse(optimizer.converged)
            self.assertAlmostEqual(optimizer.best_genome.fitness, 69.0)

        optimizer.next()
        self.assertTrue(optimizer.converged)

    def test_creates_simulated_annealer(self):
        def fitness_func(bitstring):
            return 69.0

        optimizer = new_simulated_annealer(
            (5,),
            1,
            10,
            3,
            0.5,
            fitness_func)

        self.assertIsInstance(optimizer, BasicAnnealingOptimizer)
        self.assertFalse(optimizer.converged)

        for _ in range(2):
            optimizer.next()
            self.assertFalse(optimizer.converged)
            self.assertAlmostEqual(optimizer.best_genome.fitness, 69.0)

        optimizer.next()
        self.assertTrue(optimizer.converged)

    def test_creates_hill_climber(self):
        def fitness_func(bitstring):
            return 69.0

        optimizer = new_hill_climber(
            (5,),
            10,
            1e-5,
            fitness_func)

        self.assertIsInstance(optimizer, BasicOptimizer)
        self.assertFalse(optimizer.converged)

        for _ in range(9):
            optimizer.next()
            self.assertFalse(optimizer.converged)
            self.assertAlmostEqual(optimizer.best_genome.fitness, 69.0)

        optimizer.next()
        self.assertTrue(optimizer.converged)

    def test_creates_genetic_optimizer(self):
        def fitness_func(bitstring):
            return 69.0

        optimizer = new_genetic_optimizer(
            (5,),
            100,
            0.2,
            10,
            1e-5,
            fitness_func)

        self.assertIsInstance(optimizer, BasicGeneticOptimizer)
        self.assertFalse(optimizer.converged)

        for _ in range(9):
            optimizer.next()
            self.assertFalse(optimizer.converged)
            self.assertAlmostEqual(optimizer.best_genome.fitness, 69.0)

        optimizer.next()
        self.assertTrue(optimizer.converged)


if __name__ == '__main__':
    unittest.main()
