import unittest
from tests_housing.funtions import regressor
import pandas as pd

housing_prepared = pd.read_csv("datasets/housing/housing_prepared.csv")
housing_labels = pd.read_csv("datasets/housing/housing_labels.csv")
testing_prepared = pd.read_csv("datasets/housing/testing_prepared.csv")
testing_labels = pd.read_csv("datasets/housing/testing_labels.csv")


class Test_TestRegressor(unittest.TestCase):
    def test_linear_regression(self):
        t = regressor()
        self.assertEqual(
            t.linear_regression(
                housing_prepared, housing_labels, testing_prepared, testing_labels
            ),
            4,
        )

    def test_decision_tree_regression(self):
        t = regressor()
        self.assertEqual(
            t.decision_tree_regression(
                housing_prepared, housing_labels, testing_prepared, testing_labels
            ),
            4,
        )

    def test_random_forest_regressor(self):
        t = regressor()
        self.assertEqual(
            t.random_forest_regressor(
                housing_prepared, housing_labels, testing_prepared, testing_labels
            ),
            4,
        )


if __name__ == "__main__":
    unittest.main()
