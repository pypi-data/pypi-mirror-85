import unittest

from tunepy2 import Genome
from tunepy2.comparison import RouletteWheelComparer
from tunepy2.interfaces import AbstractRandomNumberGenerator


class TestRouletteWheelComparer(unittest.TestCase):

    def test_returns_best_model(self):
        class CustomRandom(AbstractRandomNumberGenerator):

            def random_int_array(self, minimum, maximum, shape):
                return [0]

            def random(self):
                return 0.0

        rng = CustomRandom()
        comparer = RouletteWheelComparer(rng)
        genomes = [Genome.new_default_genome((10-index,), lambda bitstring: len(bitstring)) for index in range(10)]

        for genome in genomes:
            genome.run()

        returned_model = comparer.compare(genomes)
        self.assertEqual(10, returned_model.fitness)

    def test_returns_worst_model(self):
        class CustomRandom(AbstractRandomNumberGenerator):

            def random_int_array(self, minimum, maximum, shape):
                return [9]

            def random(self):
                return 0.0

        rng = CustomRandom()
        comparer = RouletteWheelComparer(rng)
        genomes = [Genome.new_default_genome((10-index,), lambda bitstring: len(bitstring)) for index in range(10)]

        for genome in genomes:
            genome.run()

        returned_model = comparer.compare(genomes)
        self.assertEqual(1, returned_model.fitness)

    def test_returns_median_model(self):
        class CustomRandom(AbstractRandomNumberGenerator):

            def random_int_array(self, minimum, maximum, shape):
                return [5]

            def random(self):
                return 0.0

        rng = CustomRandom()
        comparer = RouletteWheelComparer(rng)
        genomes = [Genome.new_default_genome((10-index,), lambda bitstring: len(bitstring)) for index in range(10)]

        for genome in genomes:
            genome.run()

        returned_model = comparer.compare(genomes)
        self.assertEqual(5, returned_model.fitness)


if __name__ == '__main__':
    unittest.main()
