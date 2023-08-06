from tests_housing.var_dtype import dtypes
import pandas as pd
import unittest

housing = pd.read_csv("datasets/housing/housing_prepared.csv")
housing = housing.drop("Unnamed: 0", axis=1)


class Test_var_dtype(unittest.TestCase):
    def test_longitude_dtype(self):
        t = dtypes()
        self.assertEqual(t.longitude_dtype(housing), "float64")

    def test_latitude_dtype(self):
        t = dtypes()
        self.assertEqual(t.latitude_dtype(housing), "float64")

