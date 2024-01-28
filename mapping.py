import polars as pl

listings = pl.read_csv("CleanData/listings.csv")

mapping = listings.select(["make", "model", "modelId"])
mapping = mapping.with_columns(make_model=pl.col("make") + " " + pl.col("model"))
mapping = mapping.unique()

mapping.write_csv("CleanData/id_mapping.csv")
mapping.write_csv("app/data/Mappings/id_mapping.csv")
