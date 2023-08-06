import unittest

from tunepy2.interfaces.stubs import PassThroughAnnealingSchedule, PassThroughGenomeFactory, NumpyCustomRandom
from tunepy2.optimizers import BasicAnnealingOptimizer
from tunepy2.internal import Genome


class TestAnnealingOptimizer(unittest.TestCase):
    def test_worse_solution_acceptance(self):
        def fitness_func_zero(bitstring):
            return 0

        def fitness_func_one(bitstring):
            return 1

        initial_candidate = Genome(fitness_func_one, (0,))
        initial_candidate.run()

        annealing_schedule = PassThroughAnnealingSchedule(0.9, True)
        genome_builder = PassThroughGenomeFactory(Genome(fitness_func_zero, (1,)))
        rng = NumpyCustomRandom(0.0, 1)
        optimizer = BasicAnnealingOptimizer(initial_candidate, genome_builder, annealing_schedule, rng)

        optimizer.next()

        self.assertEqual(0, optimizer.best_genome.fitness)
        self.assertAlmostEqual(0.9, optimizer.temperature)

    def test_better_solution_acceptance(self):
        def fitness_func_zero(bitstring):
            return 0

        def fitness_func_one(bitstring):
            return 1

        initial_candidate = Genome(fitness_func_zero, (0,))
        initial_candidate.run()

        annealing_schedule = PassThroughAnnealingSchedule(0.9, True)
        genome_builder = PassThroughGenomeFactory(Genome(fitness_func_one, (1,)))
        rng = NumpyCustomRandom(0.0, 1)
        optimizer = BasicAnnealingOptimizer(initial_candidate, genome_builder, annealing_schedule, rng)

        optimizer.next()

        self.assertEqual(1, optimizer.best_genome.fitness)
        self.assertAlmostEqual(0.9, optimizer.temperature)

    def test_convergence(self):
        def fitness_func_zero(bitstring):
            return 0

        initial_candidate = Genome(fitness_func_zero, (0,))
        initial_candidate.run()

        annealing_schedule = PassThroughAnnealingSchedule(0.9, True)
        genome_builder = PassThroughGenomeFactory(Genome(fitness_func_zero, (1,)))
        rng = NumpyCustomRandom(0.0, 1)
        optimizer = BasicAnnealingOptimizer(initial_candidate, genome_builder, annealing_schedule, rng)

        self.assertFalse(optimizer.converged)
        self.assertAlmostEqual(0.9, optimizer.temperature)
        optimizer.next()
        self.assertTrue(optimizer.converged)
        self.assertAlmostEqual(0.9, optimizer.temperature)


if __name__ == '__main__':
    unittest.main()
