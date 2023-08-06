import unittest

from tunepy2.optimizers import BasicGeneticOptimizer
from tunepy2.optimizers.builders import BasicGeneticOptimizerBuilder
from tunepy2.interfaces.stubs import PassThroughConvergenceCriterion
from tunepy2.interfaces.stubs import PassThroughGenomeFactory
from tunepy2.random import NumpyRNG
from tunepy2 import Genome, InitialPopulationUndefinedException


class TestGeneticOptimizerBasicBuilder(unittest.TestCase):
    def test_add_to_initial_population_from_factory_returns_self(self):
        def fitness_func(bitstring):
            self.fail()
            return 0.0

        genome_factory = PassThroughGenomeFactory(Genome.new_default_genome((5,), fitness_func))
        convergence_criterion = PassThroughConvergenceCriterion(True)
        optimizer_builder = BasicGeneticOptimizerBuilder((5,),
                                                         NumpyRNG(),
                                                         genome_factory,
                                                         convergence_criterion,
                                                         fitness_func)

        returned_object = optimizer_builder.add_to_initial_population_from_factory(genome_factory, 1)
        self.assertEqual(optimizer_builder, returned_object)

    def test_add_to_initial_population_returns_self(self):
        def fitness_func(bitstring):
            self.fail()
            return 0.0

        genome_factory = PassThroughGenomeFactory(Genome.new_default_genome((5,), fitness_func))
        convergence_criterion = PassThroughConvergenceCriterion(True)
        optimizer_builder = BasicGeneticOptimizerBuilder((5,),
                                                         NumpyRNG(),
                                                         genome_factory,
                                                         convergence_criterion,
                                                         fitness_func)

        returned_object = optimizer_builder.add_to_initial_population(Genome.new_default_genome((5,), fitness_func))
        self.assertEqual(optimizer_builder, returned_object)

    def test_add_to_initial_population_from_factory_successful(self):
        def fitness_func(bitstring):
            return 69.0

        genome_factory = PassThroughGenomeFactory(Genome.new_default_genome((5,), fitness_func))
        convergence_criterion = PassThroughConvergenceCriterion(True)
        optimizer_builder = BasicGeneticOptimizerBuilder((5,),
                                                         NumpyRNG(),
                                                         genome_factory,
                                                         convergence_criterion,
                                                         fitness_func)

        optimizer = optimizer_builder \
            .add_to_initial_population_from_factory(genome_factory, 1) \
            .build()

        self.assertAlmostEqual(optimizer.best_genome.fitness, 69.0)
        self.assertIsInstance(optimizer, BasicGeneticOptimizer)

    def test_add_to_initial_population_successful(self):
        class SpyFitnessFunc:
            def __init__(self):
                self.fitness_func_executions = 0

            def fitness_func(self, bitstring):
                self.fitness_func_executions += 1
                return 69.0

        unused_spy_fitness_function_holder = SpyFitnessFunc()
        genome_factory = PassThroughGenomeFactory(
            Genome.new_default_genome((5,), unused_spy_fitness_function_holder.fitness_func))
        convergence_criterion = PassThroughConvergenceCriterion(True)
        optimizer_builder = BasicGeneticOptimizerBuilder((5,),
                                                         NumpyRNG(),
                                                         genome_factory,
                                                         convergence_criterion,
                                                         unused_spy_fitness_function_holder.fitness_func)

        spy_fitness_function_holder = SpyFitnessFunc()
        population_genome = Genome(spy_fitness_function_holder.fitness_func, (0, 0, 0, 0, 0))

        optimizer = optimizer_builder \
            .add_to_initial_population(population_genome) \
            .build()

        self.assertAlmostEqual(optimizer.best_genome.fitness, 69.0)
        self.assertEqual(spy_fitness_function_holder.fitness_func_executions, 1)
        self.assertIsInstance(optimizer, BasicGeneticOptimizer)

    def test_build_raises_exception_with_no_population(self):
        def fitness_func(bitstring):
            self.fail()
            return 0.0

        genome_factory = PassThroughGenomeFactory(
            Genome.new_default_genome((5,), fitness_func))
        convergence_criterion = PassThroughConvergenceCriterion(True)
        optimizer_builder = BasicGeneticOptimizerBuilder((5,),
                                                         NumpyRNG(),
                                                         genome_factory,
                                                         convergence_criterion,
                                                         fitness_func)

        with self.assertRaises(InitialPopulationUndefinedException):
            optimizer_builder.build()

    def test_multiple_population_add(self):
        class SpyFitnessFunc:
            def __init__(self):
                self.fitness_func_executions = 0

            def fitness_func(self, bitstring):
                self.fitness_func_executions += 1
                return 69.0

        unused_spy_fitness_function_holder = SpyFitnessFunc()
        genome_factory = PassThroughGenomeFactory(
            Genome.new_default_genome((5,), unused_spy_fitness_function_holder.fitness_func))
        convergence_criterion = PassThroughConvergenceCriterion(True)
        optimizer_builder = BasicGeneticOptimizerBuilder((5,),
                                                         NumpyRNG(),
                                                         genome_factory,
                                                         convergence_criterion,
                                                         unused_spy_fitness_function_holder.fitness_func)

        spy_fitness_function_holder = SpyFitnessFunc()
        population_genome = Genome(spy_fitness_function_holder.fitness_func, (0, 0, 0, 0, 0))

        optimizer = optimizer_builder \
            .add_to_initial_population(population_genome) \
            .build()

        self.assertAlmostEqual(optimizer.best_genome.fitness, 69.0)
        self.assertEqual(spy_fitness_function_holder.fitness_func_executions, 1)
        self.assertIsInstance(optimizer, BasicGeneticOptimizer)

        with self.assertRaises(InitialPopulationUndefinedException):
            optimizer_builder.clear().build()


if __name__ == '__main__':
    unittest.main()
