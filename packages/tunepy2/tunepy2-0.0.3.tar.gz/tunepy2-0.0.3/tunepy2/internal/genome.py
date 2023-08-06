from __future__ import annotations

from typing import List, Dict, Callable, Tuple
import numpy as np


class Genome(object):
    """
    Holds a fitness function, a bitstring, and custom arguments.
    """

    def __init__(
            self,
            fitness_func: Callable[..., float],
            bitstring: Tuple,
            *args,
            **kwargs):
        """
        Creates a new Genome.

        :param fitness_func: fitness function passed into new Genome objects that accepts a bitstring
        :param bitstring: will be passed into the fitness function
        :param args: will be passed into the fitness function
        :param kwargs: will be passed into the fitness function
        """
        self._fitness_func = fitness_func
        self._bitstring = bitstring
        self._args = args
        self._kwargs = kwargs
        self._fitness = float("-inf")

    def run(self):
        """
        Executes this Genome's fitness function and updates its fitness.
        """
        self._fitness = self._fitness_func(self._bitstring, *self._args, **self._kwargs)

    @property
    def bitstring(self) -> Tuple:
        """
        This Genome's bitstring

        :return: a tuple representing a bitstring
        """
        return self._bitstring

    @property
    def fitness(self) -> float:
        """
        This Genome's current fitness score

        :return: a float representing fitness
        """
        return self._fitness

    @staticmethod
    def new_default_genome(
            dimensions: Tuple,
            fitness_func: Callable[..., float],
            *args,
            **kwargs) -> Genome:
        """
        Creates a new Genome with a default bitstring

        :param dimensions: tuple containing dimensions of bitstring
        :param fitness_func: fitness function passed into new Genome objects that accepts a bitstring
        :param args: will be passed into the fitness function
        :param kwargs: will be passed into the fitness function
        :return:
        """
        bitstring = np.zeros(shape=dimensions, dtype='int8')
        return Genome(fitness_func, bitstring, *args, **kwargs)
