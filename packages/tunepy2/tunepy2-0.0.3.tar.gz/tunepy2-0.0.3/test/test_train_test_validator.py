import unittest
from tunepy2.validators import TrainTestValidator
from tunepy2.internal import *
from tunepy2.interfaces.stubs import *


class TestTrainTestValidator(unittest.TestCase):
    def test_dimensions_error_on_validate(self):
        data_features = \
            [[0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1],
             [2, 2, 2, 2, 2],
             [3, 3, 3, 3, 3],
             [4, 4, 4, 4, 4],
             [5, 5, 5, 5, 5]]

        data_labels = \
            [0, 1, 2, 3, 4]

        validator = TrainTestValidator(0.6)

        with self.assertRaises(DimensionsMismatchException):
            validator.validate(data_features, data_labels, None)

    def test_dimensions_error_on_data_split(self):
        data_features = \
            [[0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1],
             [2, 2, 2, 2, 2],
             [3, 3, 3, 3, 3],
             [4, 4, 4, 4, 4],
             [5, 5, 5, 5, 5]]

        data_labels = \
            [0, 1, 2, 3, 4]

        validator = TrainTestValidator(0.6)

        with self.assertRaises(DimensionsMismatchException):
            validator.split_data(data_features, data_labels)

    def test_invalid_split_too_high(self):
        data_features = \
            [[0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1],
             [2, 2, 2, 2, 2],
             [3, 3, 3, 3, 3],
             [4, 4, 4, 4, 4],
             [5, 5, 5, 5, 5]]

        data_labels = \
            [0, 1, 2, 3, 4, 5]

        validator = TrainTestValidator(1.0)

        with self.assertRaises(TrainTestSplitException):
            validator.split_data(data_features, data_labels)

    def test_invalid_split_too_low(self):
        data_features = \
            [[0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1],
             [2, 2, 2, 2, 2],
             [3, 3, 3, 3, 3],
             [4, 4, 4, 4, 4],
             [5, 5, 5, 5, 5]]

        data_labels = \
            [0, 1, 2, 3, 4, 5]

        validator = TrainTestValidator(0.0)

        with self.assertRaises(TrainTestSplitException):
            validator.split_data(data_features, data_labels)

    def test_bin_sizes(self):
        data_features = \
            [[0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1],
             [2, 2, 2, 2, 2],
             [3, 3, 3, 3, 3],
             [4, 4, 4, 4, 4]]

        data_labels = \
            [0, 1, 2, 3, 4]

        validator = TrainTestValidator(0.8)
        validator.split_data(data_features, data_labels)

        self.assertEqual(4, len(validator.training_data_labels))
        self.assertEqual(4, len(validator.training_data_features))
        self.assertEqual(1, len(validator.test_data_labels))
        self.assertEqual(1, len(validator.test_data_features))

    def test_validation_result(self):
        data_features = \
            [[0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1],
             [2, 2, 2, 2, 2],
             [3, 3, 3, 3, 3],
             [4, 4, 4, 4, 4]]

        data_labels = \
            [0, 1, 2, 3, 4]

        validator = TrainTestValidator(0.8)
        fitness = validator.validate(data_features, data_labels, ConstantFitnessLearner(69.0))
        self.assertAlmostEqual(69.0, fitness)

if __name__ == '__main__':
    unittest.main()
