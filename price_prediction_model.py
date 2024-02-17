import pickle

import numpy as np
import polars as pl
import scipy.stats as st
from sklearn.ensemble import BaggingRegressor
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeRegressor

data = pl.scan_csv("PricePredictionData/data.csv").collect()

# transform categorical columns to numerical and save the encoders
label_transformers = {}
for col in data.columns:
    if data[col].dtype == pl.String:
        label_transformers[col + "_transformer"] = LabelEncoder()
        label_transformers[col + "_transformer"] = label_transformers[
            col + "_transformer"
        ].fit(data[col])
        pickle.dump(
            label_transformers[col + "_transformer"],
            open("app/Models/label_encoders/" + col + "_transformer.pkl", "wb"),
        )

for col in data.columns:
    if data[col].dtype == pl.String:
        label_enc = pickle.load(
            open("app/Models/label_encoders/" + col + "_transformer.pkl", "rb")
        )
        data = data.with_columns(
            pl.col(col).map_elements(lambda x: label_enc.transform(np.array([x])))
        )

split_datasets = dict()
split_regressors = dict()
split_metrics = dict()
num_of_splits = 8
split_step = 100_000 / num_of_splits

# split the dataset into "num_of_splits" parts
for split in range(1, num_of_splits + 1):
    upper_b = split * split_step
    lower_b = (split - 1) * split_step
    if split == num_of_splits:
        split_datasets[f"split_{split}"] = data.filter(
            pl.col("priceUnformatted") >= lower_b
        ).drop("segment")
    else:
        split_datasets[f"split_{split}"] = data.filter(
            (pl.col("priceUnformatted") >= lower_b)
            & (pl.col("priceUnformatted") < upper_b)
        ).drop("segment")

for split_key in split_datasets.keys():
    # create the classifiers
    split_regressors[split_key + "_regressor"] = BaggingRegressor(
        estimator=DecisionTreeRegressor(
            criterion="friedman_mse",
            splitter="best",
            min_samples_leaf=15,
            min_samples_split=30,
        ),
        n_estimators=10,
        max_samples=0.4,
        max_features=0.4,
        bootstrap=False,
    )
    # target column
    target_col = split_datasets[split_key]["priceUnformatted"]
    # compute cross validation scores
    cv_losses = np.sqrt(
        -cross_val_score(
            split_regressors[split_key + "_regressor"],
            split_datasets[split_key].drop("priceUnformatted").to_numpy(),
            target_col.to_numpy(),
            cv=10,
            scoring="neg_mean_squared_error",
        )
    )
    # store the 95% confidence intervals for the error of each classifier
    split_metrics[split_key + "_metrics"] = st.t.interval(
        confidence=0.95,
        df=len(cv_losses) - 1,
        loc=np.mean(cv_losses),
        scale=st.sem(cv_losses),
    )
    # train each classifier on their segment
    split_regressors[split_key + "_regressor"].fit(
        split_datasets[split_key].drop("priceUnformatted"), target_col
    )

# save the trained regressors and confidence intervals
for key in split_regressors.keys():
    pickle.dump(
        split_regressors[key],
        open("app/Models/price_pred_models/" + key + ".pkl", "wb"),
    )

for key in split_metrics.keys():
    pickle.dump(
        split_metrics[key], open("app/Models/model_intervals/" + key + ".pkl", "wb")
    )
