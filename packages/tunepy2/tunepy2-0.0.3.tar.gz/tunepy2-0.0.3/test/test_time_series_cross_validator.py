import unittest

from tunepy2.interfaces.stubs import ConstantFitnessLearner
from tunepy2.validators import TimeSeriesCrossValidator
from tunepy2 import TimeSeriesCrossValidatorBinException, DimensionsMismatchException


class TestTimeSeriesCrossValidator(unittest.TestCase):
    def test_bin_creation_error(self):
        validator = TimeSeriesCrossValidator(1)

        with self.assertRaises(TimeSeriesCrossValidatorBinException):
            validator.validate(None, None, None)

    def test_dimensions_mismatch_error_on_build(self):
        data_features = \
            [[0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1],
             [2, 2, 2, 2, 2],
             [3, 3, 3, 3, 3],
             [4, 4, 4, 4, 4],
             [5, 5, 5, 5, 5]]

        data_labels = \
            [0, 1, 2, 3, 4]

        validator = TimeSeriesCrossValidator(5)

        with self.assertRaises(DimensionsMismatchException):
            validator.build_bins(data_features, data_labels)

    def test_dimensions_mismatch_error_on_validate(self):
        data_features = \
            [[0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1],
             [2, 2, 2, 2, 2],
             [3, 3, 3, 3, 3],
             [4, 4, 4, 4, 4],
             [5, 5, 5, 5, 5]]

        data_labels = \
            [0, 1, 2, 3, 4]

        validator = TimeSeriesCrossValidator(5)

        with self.assertRaises(DimensionsMismatchException):
            validator.validate(data_features, data_labels, None)

    def test_bin_sizes(self):
        data_features = \
            [[0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1],
             [2, 2, 2, 2, 2],
             [3, 3, 3, 3, 3],
             [4, 4, 4, 4, 4],
             [5, 5, 5, 5, 5]]

        data_labels = \
            [0, 1, 2, 3, 4, 5]

        validator = TimeSeriesCrossValidator(5)
        validator.build_bins(data_features, data_labels)

        self.assertEqual(5, len(validator.feature_bins))
        self.assertEqual(5, len(validator.label_bins))

        self.assertEqual(1, len(validator.feature_bins[0]))
        self.assertEqual(1, len(validator.label_bins[0]))

        self.assertEqual(2, len(validator.feature_bins[-1]))
        self.assertEqual(2, len(validator.label_bins[-1]))

    def test_validation_result(self):
        data_features = \
            [[0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1],
             [2, 2, 2, 2, 2],
             [3, 3, 3, 3, 3],
             [4, 4, 4, 4, 4]]

        data_labels = \
            [0, 1, 2, 3, 4]

        validator = TimeSeriesCrossValidator(5)
        fitness = validator.validate(data_features, data_labels, ConstantFitnessLearner(69.0))
        self.assertAlmostEqual(69.0, fitness)

    def test_bin_count(self):
        validator = TimeSeriesCrossValidator(10)
        self.assertEqual(10, validator.bins)

if __name__ == '__main__':
    unittest.main()
