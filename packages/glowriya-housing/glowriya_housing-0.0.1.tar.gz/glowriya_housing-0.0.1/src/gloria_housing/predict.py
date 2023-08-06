import logging

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

logging.basicConfig(
    filename="predict_log.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(name)s - %(message)s",
)
housing = pd.read_csv("datasets/housing/housing_prepared.csv")
testing = pd.read_csv("datasets/housing/testing_prepared.csv")

housing = housing.drop("Unnamed: 0", axis=1)
x_train = housing.drop("median_house_value", axis=1)
y_train = housing["median_house_value"]

testing = testing.drop("Unnamed: 0", axis=1)
x_test = testing.drop("median_house_value", axis=1)
y_test = testing["median_house_value"]


def predict_linear_regression(x_train, y_train, x_test):
    """ Predicts the median hosing value 
        using linear regression
    """
    lin_reg = LinearRegression()
    lin_reg.fit(x_train, y_train)
    housing_predictions = lin_reg.predict(x_test)
    return housing_predictions


def predict_decision_tree_regression(x_train, y_train, x_test):
    """ Predicts the median hosing value 
        using decision tree regression
    """
    tree_reg = DecisionTreeRegressor(random_state=42)
    tree_reg.fit(x_train, y_train)
    housing_predictions = tree_reg.predict(x_test)
    return housing_predictions


def predict_random_forest_regressor(x_train, y_train, x_test, y_test):
    """ Predicts the median hosing value 
        using random forest regression
    """
    forest_reg = RandomForestRegressor(max_features=6, n_estimators=30, random_state=42)
    forest_reg.fit(x_train, y_train)
    final_predictions = forest_reg.predict(x_test)
    return final_predictions


lin_reg_pred = predict_linear_regression(x_train, y_train, x_test)
logging.info("Predicted linear regression model")

dec_tree_pred = predict_decision_tree_regression(x_train, y_train, x_test)
logging.info("Predicted decision tree model")

ran_for_pred = predict_random_forest_regressor(x_train, y_train, x_test, y_test)
logging.info("Predicted random forest model")

