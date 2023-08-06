import unittest
from tunepy2.convergence import ConsecutiveNonImprovement


class TestConsecutiveNonImprovement(unittest.TestCase):
    def test_divergence(self):
        class FakeGenome:
            def __init__(self, fitness):
                self._fitness = fitness

            @property
            def fitness(self):
                return self._fitness

        convergence = ConsecutiveNonImprovement(5, 2)

        old_genome = FakeGenome(-1)
        for index in range(20):
            new_genome = FakeGenome(index)
            self.assertFalse(convergence.converged(old_genome, new_genome))
            old_genome = new_genome

    def test_convergence(self):
        class FakeGenome:
            def __init__(self, fitness):
                self._fitness = fitness

            @property
            def fitness(self):
                return self._fitness

        convergence = ConsecutiveNonImprovement(5, 1e-5)

        old_genome = FakeGenome(-1)
        for index in range(4):
            self.assertFalse(convergence.converged(old_genome, old_genome))
        self.assertTrue(convergence.converged(old_genome, old_genome))


if __name__ == '__main__':
    unittest.main()
