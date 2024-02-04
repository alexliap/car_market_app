import pickle

import numpy as np
import polars as pl


def get_pred(
    data,
    make,
    modelId,
    year,
    mileage=None,
    cylinders=None,
    displacement=None,
    hp=None,
    torque=None,
    highway_mpg=None,
    city_mpg=None,
    condition=None,
    bodyStyle=None,
    configuration_engine=None,
    fuel=None,
    transmission=None,
    drivenWheels=None,
    market_categories=None,
):
    # fields the user is going to pass to the app to get a suggestion
    filter_dict = {
        "year": year,
        "modelId": modelId,
        "mileageUnformatted": mileage,
        "cylinder_engine": cylinders,
        "size_engine": displacement,
        "horsepower_engine": hp,
        "torque_engine": torque,
        "highway_mpg": highway_mpg,
        "city_mpg": city_mpg,
        "make": make,
        "condition": condition,
        "bodyStyle": bodyStyle,
        "configuration_engine": configuration_engine,
        "type_engine": fuel,
        "name_transmission": transmission,
        "drivenWheels": drivenWheels,
        "market_categories": market_categories,
    }

    filter_dict = encode_input(filter_dict)
    rule_dict = find_rule()

    data = pl.from_pandas(data)
    data = encode_dataset(data)
    # turn fields to an array in order to make the prediction
    query = pl.from_dict(filter_dict)
    # filter the dataset in order to get the correct vehicle
    for key in filter_dict.keys():
        if filter_dict[key] is not None:
            if key in rule_dict.keys():
                data = data.filter(
                    (pl.col(key) >= filter_dict[key] - rule_dict[key])
                    & (pl.col(key) <= filter_dict[key] + rule_dict[key])
                )
            else:
                data = data.filter(pl.col(key) == filter_dict[key])
    # find the segments the vehicle belongs to
    data = (
        data["segment"]
        .value_counts()
        .sort("segment")
        .with_columns(freq=pl.col("count") / len(data))
        .drop("count")
    )

    queried_regressors = []
    queried_metrics = []
    # get the correct regressors and confidence intervals
    for i in data["segment"]:
        i = int(i)
        queried_regressors.append(
            pickle.load(
                open(
                    "app/Models/price_pred_models/split_" + str(i) + "_regressor.pkl",
                    "rb",
                )
            )
        )
        queried_metrics.append(
            pickle.load(
                open(
                    "app/Models/model_intervals/split_" + str(i) + "_metrics.pkl", "rb"
                )
            )
        )

    # make the prediction
    prediction = 0
    upper_bound = 0
    lower_bound = 0
    for j in range(len(data)):
        prediction += data["freq"][j] * queried_regressors[j].predict(query).item()
        upper_bound += data["freq"][j] * queried_metrics[j][1]
        lower_bound += data["freq"][j] * queried_metrics[j][0]

    prediction = int(np.round(prediction))
    upper_bound = int(np.round(upper_bound))
    lower_bound = int(np.round(lower_bound))

    return prediction, upper_bound, lower_bound


def encode_dataset(dataset):
    for col in dataset.columns:
        if dataset[col].dtype == pl.String:
            label_enc = pickle.load(
                open("app/Models/label_encoders/" + col + "_transformer.pkl", "rb")
            )
            dataset = dataset.with_columns(
                pl.col(col).map_elements(lambda x: label_enc.transform(np.array([x])))
            )

    return dataset


def encode_input(filter_dict: dict):
    vars_for_encoding = [
        "make",
        "name_transmission",
        "bodyStyle",
        "condition",
        "configuration_engine",
        "drivenWheels",
        "market_categories",
        "type_engine",
    ]

    for var in vars_for_encoding:
        if filter_dict[var] is not None:
            encoder = pickle.load(
                open("app/Models/label_encoders/" + var + "_transformer.pkl", "rb")
            )
            filter_dict[var] = encoder.transform(np.array([filter_dict[var]])).item()

    return filter_dict


def find_rule():
    rule_dict = {
        "year": 2,
        "mileageUnformatted": 30_000,
        "size_engine": 0.5,
        "horsepower_engine": 40,
    }

    return rule_dict
