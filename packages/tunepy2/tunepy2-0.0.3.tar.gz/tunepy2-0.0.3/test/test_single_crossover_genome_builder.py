import unittest
from tunepy2.genome_factory import SinglePointCrossoverGenomeFactory
from tunepy2.interfaces.stubs import IncrementalComparer, NumpyOnesRandom, NumpyPassThroughRandom, NumpyCustomRandom
from tunepy2.internal import DimensionsMismatchException, Genome
import numpy as np


class TestSingleCrossoverGenomeBuilder(unittest.TestCase):
    def test_incorrect_dimensions_passed_in(self):
        def fitness_func(bitstring):
            return 0.0

        left = Genome(fitness_func, (0, 0, 0, 0, 0))
        right = Genome(fitness_func, (1, 1, 1, 1, 1))
        dimensions = (4,)

        comparer = IncrementalComparer()
        rng = NumpyOnesRandom()
        genome_builder = SinglePointCrossoverGenomeFactory(dimensions, rng, 0.0, comparer, fitness_func)

        with self.assertRaises(DimensionsMismatchException):
            genome_builder.build([left, right])

    def test_mutation(self):
        def fitness_func(bitstring):
            return 0.0

        left = Genome(fitness_func, (0, 0, 0, 0, 0))
        right = Genome(fitness_func, (0, 0, 0, 0, 0))
        dimensions = (5,)

        comparer = IncrementalComparer()
        rng = NumpyCustomRandom(0.1, 1)
        genome_builder = SinglePointCrossoverGenomeFactory(dimensions, rng, 1.0, comparer, fitness_func)

        new_genome = genome_builder.build([left, right])

        self.assertEqual([1, 1, 1, 1, 1], list(new_genome.bitstring))

    def test_inheritance(self):
        def fitness_func(bitstring):
            return 0.0

        left = Genome(fitness_func, 2 * np.ones((2, 6)))
        right = Genome(fitness_func, 3 * np.ones((2, 6)))
        dimensions = (2, 6)

        comparer = IncrementalComparer()
        rng = NumpyPassThroughRandom(3)
        genome_builder = SinglePointCrossoverGenomeFactory(dimensions, rng, 0.0, comparer, fitness_func)

        expected = np.ones((2, 6))
        expected[:, 3:] = 3
        expected[:, :3] = 2

        new_genome = genome_builder.build([left, right])

        self.assertTrue(np.array_equal(expected, new_genome.bitstring))


if __name__ == '__main__':
    unittest.main()
