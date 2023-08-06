import logging

import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor

logging.basicConfig(
    filename="train_score_model.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(name)s - %(message)s",
)
housing_prepared = pd.read_csv("datasets/housing/housing_prepared.csv")

housing = housing_prepared.drop("Unnamed: 0", axis=1)
x = housing.drop("median_house_value", axis=1)
y = housing["median_house_value"]

models = []

models.append(("Linear Regression", LinearRegression()))
models.append(("Decision Tree Regressor", DecisionTreeRegressor(random_state=42)))
models.append(
    (
        "Random Forest regressor",
        RandomForestRegressor(max_features=6, n_estimators=30, random_state=42),
    )
)
seed = 7
results = []
names = []
logging.debug("Started training models")
for name, model in models:
    kfold = model_selection.KFold(n_splits=10, random_state=seed, shuffle=True)
    scoring = "neg_mean_squared_error"
    result = model_selection.cross_val_score(model, x, y, scoring=scoring, cv=kfold)
    logging.info("Scored model %s" % (name))
    results.append(result)
    names.append(name)
    msg = "%s: %f (%f)" % (name, result.mean(), result.std())
    print(msg)

