import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

housing = pd.read_csv("datasets/housing/housing_prepared.csv")
housing = housing.drop("Unnamed: 0", axis=1)
x_train = housing.drop("median_house_value", axis=1)
y_train = housing["median_house_value"]


forest_reg = RandomForestRegressor(max_features=6, n_estimators=30, random_state=42)
forest_reg.fit(x_train, y_train)


def predict_median(x_test):
    """ Predicts the median hosing value 
        using random forest regression
    """
    predictions = forest_reg.predict(x_test)
    return predictions


def score(x_test, y_test):
    """ return the score of pre-trained model
    """
    predictions = forest_reg.predict(x_test)
    mse = mean_squared_error(y_test, predictions)
    return mse

