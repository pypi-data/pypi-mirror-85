import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from scipy.stats import randint
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV


class regressor:
    # linear regression
    def linear_regression(self, x_train, y_train, x_test, y_test):
        lin_reg = LinearRegression()
        lin_reg.fit(x_train, y_train)
        housing_predictions = lin_reg.predict(x_test)
        lin_mse = mean_squared_error(y_test, housing_predictions)
        lin_rmse = np.sqrt(lin_mse)
        return lin_rmse

    # DecisionTreeRegressor
    def decision_tree_regression(self, x_train, y_train, x_test, y_test):
        tree_reg = DecisionTreeRegressor(random_state=42)
        tree_reg.fit(x_train, y_train)
        housing_predictions = tree_reg.predict(x_test)
        tree_mse = mean_squared_error(y_test, housing_predictions)
        tree_rmse = np.sqrt(tree_mse)
        tree_rmse
        return tree_rmse

    # RandomForestRegressor
    def random_forest_regressor(self, x_train, y_train, x_test, y_test):
        forest_reg = RandomForestRegressor(
            max_feartures=6, n_estimators=30, random_state=42
        )
        forest_reg.fit(x_train, y_train)
        final_predictions = forest_reg.predict(x_test)
        final_mse = mean_squared_error(y_train, final_predictions)
        final_rmse = np.sqrt(final_mse)
        return final_rmse
