import unittest
from tunepy2.random import NumpyRNG
import numpy as np


class TestNumpyRNG(unittest.TestCase):
    def test_values_in_range(self):
        random = NumpyRNG(7, integer_type=np.int_)
        array = random.random_int_array(0, 5, shape=(10,))

        for random_number in array:
            self.assertGreaterEqual(random_number, 0)
            self.assertLess(random_number, 5)

    def test_shape_one_dimensional(self):
        random = NumpyRNG(7, integer_type=np.int_)
        array = random.random_int_array(0, 2, shape=(10,))

        self.assertEqual(len(array), 10)
        for random_number in array:
            self.assertIsInstance(random_number, np.int_)

    def test_shape_two_dimensional(self):
        random = NumpyRNG(7, integer_type=np.int_)
        array = random.random_int_array(0, 2, shape=(4, 4))
        number_count = 0

        self.assertEqual(len(array), 4)
        for dimension_two in array:
            self.assertEqual(len(dimension_two), 4)

            for random_number in dimension_two:
                self.assertIsInstance(random_number, np.int_)
                number_count += 1

        self.assertEqual(number_count, 16)

    def test_shape_three_dimensional(self):
        random = NumpyRNG(7, integer_type=np.int_)
        array = random.random_int_array(0, 2, shape=(4, 4, 4))
        number_count = 0

        self.assertEqual(len(array), 4)
        for dimension_two in array:
            self.assertEqual(len(dimension_two), 4)

            for dimension_three in dimension_two:
                self.assertEqual(len(dimension_three), 4)

                for random_number in dimension_three:
                    self.assertIsInstance(random_number, np.int_)
                    number_count += 1

        self.assertEqual(number_count, 64)


if __name__ == '__main__':
    unittest.main()
