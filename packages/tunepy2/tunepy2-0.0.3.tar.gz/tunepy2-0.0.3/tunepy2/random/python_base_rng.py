from typing import Tuple

from tunepy2.interfaces import AbstractRandomNumberGenerator
import random


class PythonBaseRNG(AbstractRandomNumberGenerator):
    """
    A tunepy2 wrapper of the built in Python random number generator.
    """

    def __init__(self, seed):
        """
        Creates a new PythonBaseRNG.

        :param seed: seed passed into python's random
        """
        random.seed(seed)

    def random(self) -> float:
        """
        Returns a random number between 0 and 1

        :return: random number between 0 and 1
        """
        return random.random()

    def random_int_array(self, minimum: int, maximum: int, shape: Tuple) -> Tuple:
        """
        Builds an array-like structure of random integers

        :param minimum: minimum value (inclusive)
        :param maximum: maximum value (exclusive)
        :param shape: the shape of the output
        :return: a collection of integers
        """

        def traverse_next_dimension(new_shape, array):
            if len(new_shape) == 1:
                append_new_random_vector(new_shape[0], array)
            else:
                append_new_list_and_recurse(new_shape, array)

        def append_new_random_vector(length, array):
            for _ in range(length):
                array.append(random.randrange(minimum, maximum))

        def append_new_list_and_recurse(new_shape, array):
            for _ in range(new_shape[0]):
                array.append([])
                traverse_next_dimension(new_shape[1:], array[-1])

        return_array = []
        traverse_next_dimension(shape, return_array)
        return tuple(return_array)
