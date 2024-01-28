import polars as pl
from sklearn.cluster import HDBSCAN

features = pl.read_csv("CleanData/features.csv")
listings = pl.read_csv("CleanData/listings.csv")
mapping = pl.read_csv("CleanData/id_mapping.csv")

features = features.drop(
    [
        "id_make",
        "niceName_make",
        "niceName_model",
        "id_engine",
        "id_transmission",
        "name_transmission",
        "numberOfSpeeds_transmission",
        "vehicleType_categories",
        "vehicleStyle_categories",
        "automaticType_transmission",
        "errorType",
        "message",
    ]
)

new_data = (
    listings.select(["vin", "modelId", "priceUnformatted"])
    .join(features, on="vin", how="inner")
    .drop("vin")
)

num_cols = new_data.select(pl.col([pl.Float64, pl.Int64])).drop("modelId").columns
str_cols = new_data.select(pl.col(pl.String)).columns
cls_data = new_data

for col in num_cols:
    mean = cls_data[col].mean()
    std = cls_data[col].std()

    cls_data = cls_data.with_columns(((cls_data[col] - mean) / std).alias(col))

cls_data = cls_data.to_dummies(str_cols)

hdb = HDBSCAN(
    min_cluster_size=40,
    metric="euclidean",
    algorithm="auto",
    n_jobs=4,
    max_cluster_size=100,
    cluster_selection_method="leaf",
    leaf_size=50,
)
hdb.fit(cls_data)

cls_data = cls_data.with_columns(segment=hdb.labels_)
cls_data = cls_data.join(mapping, on="modelId", how="inner").drop(["make", "model"])

cls_data.write_csv("ClusteringData/data.csv")
cls_data.write_csv("app/data/ClusteringData/data.csv")
