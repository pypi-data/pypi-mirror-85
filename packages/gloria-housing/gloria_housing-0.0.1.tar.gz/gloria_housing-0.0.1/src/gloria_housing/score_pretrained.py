import logging

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.tree import DecisionTreeRegressor

logging.basicConfig(
    filename="score_pretrained.log",
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


def linear_regression(x_train, y_train, x_test, y_test):
    """ returns score from pre-trained
    linear regression model
    """
    lin_reg = LinearRegression()
    lin_reg.fit(x_train, y_train)
    housing_predictions = lin_reg.predict(x_test)
    lin_mse = mean_squared_error(y_test, housing_predictions)
    return lin_mse


def decision_tree_regression(x_train, y_train, x_test, y_test):
    """ returns score from pre-trained
    decision tree regression model
    """
    tree_reg = DecisionTreeRegressor()
    tree_reg.fit(x_train, y_train)
    housing_predictions = tree_reg.predict(x_test)
    tree_mse = mean_squared_error(y_test, housing_predictions)
    return tree_mse


def random_forest_regressor(x_train, y_train, x_test, y_test):
    """ returns score from pre-trained
    random forest regression model
    """
    forest_reg = RandomForestRegressor()
    forest_reg.fit(x_train, y_train)
    final_predictions = forest_reg.predict(x_test)
    final_mse = mean_squared_error(y_test, final_predictions)
    return final_mse


lin_reg_mse = linear_regression(x_train, y_train, x_test, y_test)
logging.info("Scored linear regression model")

dec_tree_mse = decision_tree_regression(x_train, y_train, x_test, y_test)
logging.info("Scored decision tree model")

ran_for_mse = random_forest_regressor(x_train, y_train, x_test, y_test)
logging.info("Scored random forest model")

print(f"Linear Regression: {lin_reg_mse}")
print(f"Decision Tree Regressor: {dec_tree_mse}")
print(f"Random Forest Regressor: {ran_for_mse}")
