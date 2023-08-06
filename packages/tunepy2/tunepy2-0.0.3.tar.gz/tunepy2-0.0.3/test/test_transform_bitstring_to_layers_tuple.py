import unittest
import numpy as np
from tunepy2 import transform_bitstring_to_layers_tuple


class TestTransformBitstringToLayersTuple(unittest.TestCase):
    def test_one_dimension_ones(self):
        bitstring = np.ones(shape=(1, 10), dtype=int)
        layers = transform_bitstring_to_layers_tuple(bitstring)
        self.assertEqual(10, layers.shape[0])
        self.assertEqual(10, layers.sum())
        self.assertEqual(0, layers[layers > 1].shape[0])
        self.assertEqual(0, layers[layers < 1].shape[0])

    def test_one_dimension_ones_missing_one(self):
        bitstring = np.ones(shape=(1, 10), dtype=int)
        bitstring[0, 1] = 0
        layers = transform_bitstring_to_layers_tuple(bitstring)
        self.assertEqual(9, layers.shape[0])
        self.assertEqual(9, layers.sum())
        self.assertEqual(0, layers[layers > 1].shape[0])
        self.assertEqual(0, layers[layers < 1].shape[0])

    def test_two_dimension_ones(self):
        bitstring = np.ones(shape=(5, 10), dtype=int)
        layers = transform_bitstring_to_layers_tuple(bitstring)
        self.assertEqual(10, layers.shape[0])
        self.assertEqual(50, layers.sum())
        self.assertEqual(10, layers[layers > 1].shape[0])
        self.assertEqual(0, layers[layers < 1].shape[0])

    def test_two_dimension_ones_missing_one(self):
        bitstring = np.ones(shape=(5, 10), dtype=int)
        bitstring[:, 1] = 0
        layers = transform_bitstring_to_layers_tuple(bitstring)
        self.assertEqual(9, layers.shape[0])
        self.assertEqual(45, layers.sum())
        self.assertEqual(9, layers[layers > 1].shape[0])
        self.assertEqual(0, layers[layers < 1].shape[0])


if __name__ == '__main__':
    unittest.main()
