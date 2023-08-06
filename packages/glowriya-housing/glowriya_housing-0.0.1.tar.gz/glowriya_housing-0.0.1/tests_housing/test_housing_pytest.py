from tests_housing.funtions import regressor
import pandas as pd
from sklearn.model_selection import train_test_split

housing = pd.read_csv("datasets/housing/housing_prepared.csv")

housing = housing.drop("Unnamed: 0", axis=1)
train, test = train_test_split(housing, test_size=0.2, random_state=42)

x_train = train.drop("median_house_value", axis=1)
y_train = train["median_house_value"]
x_test = test.drop("median_house_value", axis=1)
y_test = test["median_house_value"]


def test_linear_regression():
    t = regressor()
    assert t.linear_regression(x_train, y_train, x_test, y_test) == 4


def test_decision_tree_regression():
    t = regressor()
    assert t.decision_tree_regression(x_train, y_train, x_test, y_test) == 4


def test_random_forest_regressor():
    t = regressor()
    assert t.random_forest_regressor(x_train, y_train, x_test, y_test) == 4

