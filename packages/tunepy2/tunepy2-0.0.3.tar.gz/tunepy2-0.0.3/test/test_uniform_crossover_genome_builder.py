import unittest
from tunepy2.interfaces.stubs import IncrementalComparer, NumpyOnesRandom, NumpyPassThroughRandom
from tunepy2.internal import DimensionsMismatchException, Genome
from tunepy2.genome_factory import UniformCrossoverGenomeFactory
import numpy as np


class TestUniformCrossoverGenomeBuilder(unittest.TestCase):
    def test_incorrect_dimensions_passed_in(self):
        def fitness_func(bitstring):
            return 0.0

        left = Genome(fitness_func, (0, 0, 0, 0, 0))
        right = Genome(fitness_func, (1, 1, 1, 1, 1))
        dimensions = (4,)

        comparer = IncrementalComparer()
        rng = NumpyOnesRandom()
        genome_builder = UniformCrossoverGenomeFactory(dimensions, rng, 0.0, comparer, fitness_func)

        with self.assertRaises(DimensionsMismatchException):
            genome_builder.build([left, right])

    def test_mutation(self):
        def fitness_func(bitstring):
            return 0.0

        left = Genome(fitness_func, (0, 0, 0, 0, 0))
        right = Genome(fitness_func, (0, 0, 0, 0, 0))
        dimensions = (5,)

        comparer = IncrementalComparer()
        rng = NumpyOnesRandom()
        genome_builder = UniformCrossoverGenomeFactory(dimensions, rng, 1.0, comparer, fitness_func)

        new_genome = genome_builder.build([left, right])

        self.assertEqual([1, 1, 1, 1, 1], list(new_genome.bitstring))

    def test_left_inheritance(self):
        def fitness_func(bitstring):
            return 0.0

        left = Genome(fitness_func, 2 * np.ones((5, 5)))
        right = Genome(fitness_func, 3 * np.ones((5, 5)))
        dimensions = (5, 5)

        comparer = IncrementalComparer()
        rng = NumpyPassThroughRandom(0.2)
        genome_builder = UniformCrossoverGenomeFactory(dimensions, rng, 0.0, comparer, fitness_func)

        new_genome = genome_builder.build([left, right])

        self.assertTrue(np.array_equal(left.bitstring, new_genome.bitstring))

    def test_right_inheritance(self):
        def fitness_func(bitstring):
            return 0.0

        left = Genome(fitness_func, 2 * np.ones((5, 5)))
        right = Genome(fitness_func, 3 * np.ones((5, 5)))
        dimensions = (5, 5)

        comparer = IncrementalComparer()
        rng = NumpyPassThroughRandom(0.8)
        genome_builder = UniformCrossoverGenomeFactory(dimensions, rng, 0.0, comparer, fitness_func)

        new_genome = genome_builder.build([left, right])

        self.assertTrue(np.array_equal(right.bitstring, new_genome.bitstring))


if __name__ == '__main__':
    unittest.main()
