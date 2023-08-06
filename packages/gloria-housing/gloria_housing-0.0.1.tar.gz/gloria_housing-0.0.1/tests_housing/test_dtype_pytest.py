from tests_housing.var_dtype import dtypes
import pandas as pd

housing = pd.read_csv("datasets/housing/housing_prepared.csv")
housing = housing.drop("Unnamed: 0", axis=1)


def test_longitude_dtype():
    t = dtypes()
    assert t.longitude_dtype(housing) == "float64"


def test_latitude_dtype():
    t = dtypes()
    assert t.latitude_dtype(housing) == "float64"

