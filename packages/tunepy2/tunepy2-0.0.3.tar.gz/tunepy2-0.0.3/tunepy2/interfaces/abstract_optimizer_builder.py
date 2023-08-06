from __future__ import annotations

from abc import ABC, abstractmethod
from tunepy2 import Genome
from tunepy2.interfaces import AbstractGenomeFactory, AbstractOptimizer


class AbstractOptimizerBuilder(ABC):
    """
    Common interface for all optimizers.
    """

    @abstractmethod
    def add_to_initial_population_from_factory(
            self,
            genome_factory: AbstractGenomeFactory,
            n: int) -> AbstractOptimizerBuilder:
        """
        Adds a given number of Genomes to the initial population of this optimizer from a factory

        :param genome_factory: the factory that will generate the Genome
        :param n: number of instances to add
        :return: self
        """
        pass

    @abstractmethod
    def add_to_initial_population(self, genome: Genome) -> AbstractOptimizerBuilder:
        """
        Adds a single Genome instance to the initial population of this optimizer

        :param genome: instance to add
        :return: self
        """
        pass

    @abstractmethod
    def build(self) -> AbstractOptimizer:
        """
        Constructs a new optimizer

        :return: a new optimizer
        """
        pass

    @abstractmethod
    def clear(self) -> AbstractOptimizerBuilder:
        """
        Clears the initial population of this builder

        :return: self
        """
        pass
