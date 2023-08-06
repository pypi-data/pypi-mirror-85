from abc import ABC, abstractmethod
from typing import List

from tunepy2 import Genome


class AbstractGenomeComparer(ABC):
    """
    Interface for comparing multiple Genomes
    """

    @abstractmethod
    def compare(self, genomes: List[Genome]) -> Genome:
        """ Compares a list of Genomes and returns a single Genome

        :param genomes: list of Genome objects to compare
        :return: Genome. the result of comparing all genomes
        """
        pass
