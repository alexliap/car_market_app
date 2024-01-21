import pandas as pd
from sklearn.preprocessing import LabelEncoder

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
]
mrg_data.drop(columns_to_drop, inplace=True, axis=1)

# drop compressorType_engine because more than half of the values are missing
mrg_data.drop("compressorType_engine", axis=1, inplace=True)

str_cols = mrg_data.select_dtypes(include="object")
str_cols = str_cols.apply(LabelEncoder().fit_transform)

num_cols = mrg_data.select_dtypes(exclude="object")

result = pd.concat([num_cols, str_cols], axis=1)

result.to_csv("PricePredictionData/data.csv", index=False)

print(f"Price prediction data saved: Shape {result.shape}")
