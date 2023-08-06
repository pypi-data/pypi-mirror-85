from tunepy2.interfaces import AbstractGenomeFactory
from copy import deepcopy


class PassThroughGenomeFactory(AbstractGenomeFactory):
    def __init__(self, returned_genome):
        self._genome = returned_genome
        self._dimensions = ()

    def build(self, prior_genomes):
        return deepcopy(self._genome)

    @property
    def dimensions(self):
        return self._dimensions
