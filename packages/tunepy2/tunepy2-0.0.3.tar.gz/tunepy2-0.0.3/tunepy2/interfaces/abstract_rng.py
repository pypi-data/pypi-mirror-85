from abc import ABC, abstractmethod
from typing import Tuple


class AbstractRandomNumberGenerator(ABC):
    """
    The common interface for that tunepy2 expects from all random number generators.
    """

    @abstractmethod
    def random_int_array(self, minimum: int, maximum: int, shape: Tuple) -> Tuple:
        """
        Builds an array-like structure of random integers

        :param minimum: minimum value (inclusive)
        :param maximum: maximum value (exclusive)
        :param shape: the shape of the output
        :return: a collection of integers
        """
        pass

    @abstractmethod
    def random(self) -> float:
        """
        Returns a random number between 0 and 1

        :return: random number between 0 and 1
        """
        pass

    def random_int(self, minimum: int, maximum: int) -> int:
        """
        Returns a single random integer

        :param minimum: minimum value (inclusive)
        :param maximum: maximum value (exclusive)
        :return: random integer
        """
        return self.random_int_array(minimum, maximum, shape=(1,))[0]
