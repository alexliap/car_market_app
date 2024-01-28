import polars as pl

features = pl.read_csv("CleanData/features.csv")
listings = pl.read_csv("CleanData/listings.csv")

mapping = listings.select(["make", "model", "modelId"])
mapping = mapping.with_columns(make_model=pl.col("make") + " " + pl.col("model")).drop(
    ["make", "model"]
)
mapping = mapping.unique()
mapping.write_csv("CleanData/id_mapping.csv")
