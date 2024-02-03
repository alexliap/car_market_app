import pandas as pd
import polars as pl
import polars.selectors as cs

listings = pd.read_csv("CleanData/listings.csv")
features = pd.read_csv("CleanData/features.csv")

mrg_data = listings.merge(features, on="vin")

# columns not to be used for price prediction
columns_to_drop = [
    "vin",
    "model",
    "id_make",
    "niceName_make",
    "niceName_model",
    "id_engine",
    "compressionRatio_engine",
    "id_transmission",
    "transmissionType_transmission",
    "numberOfSpeeds_transmission",
    "epaClass_categories",
    "vehicleType_categories",
    "vehicleStyle_categories",
    "automaticType_transmission",
    "errorType",
    "message",
    "compressorType_engine",
]
mrg_data.drop(columns_to_drop, inplace=True, axis=1)

# change values in some columns to be prettier in the app
mrg_data = mrg_data.replace("electrically variableA", "Electrically Variable")
mrg_data = mrg_data.replace("continuously variableA", "Continuously Variable")

mrg_data = mrg_data.replace(["four wheel drive", "all wheel drive"], "AWD")
mrg_data = mrg_data.replace("front wheel drive", "FWD")
mrg_data = mrg_data.replace("rear wheel drive", "RWD")

# create a segment column
result = pl.from_pandas(mrg_data)
num_of_splits = 8
split_step = 100_000 / num_of_splits
for i in range(1, num_of_splits + 1):
    result = result.with_columns(
        pl.when(pl.col("priceUnformatted") < split_step * i)
        .then(pl.lit(i))
        .otherwise(pl.lit(None))
        .alias("segment_" + str(i))
    )
result = result.with_columns(
    segment=pl.min_horizontal(cs.starts_with("segment_"))
).drop(cs.starts_with("segment_"))

result.write_csv("PricePredictionData/data.csv")
result.write_csv("app/data/PricePredictionData/data.csv")

print(f"Price prediction data saved: Shape {result.shape}")
