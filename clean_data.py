import pandas as pd

listings = pd.read_csv("RawData/data.csv")
feat_data = pd.read_csv("RawData/features_data.csv")

# columns that cannot be used for price prediction from 'listings' DataFrame
columns_to_drop = [
    "displayColor",
    "city",
    "lat",
    "lon",
    "regionName",
    "experience",
    "priceMobile",
    "recentPriceDrop",
    "eligibleForFinancing",
    "financingExperience",
    "isHot",
    "newPriceAsMsrp",
    "active",
    "state",
    "trim",
    "monthlyPayment",
    "bodyType",
    "mileage",
    "mileageHumanized",
    "showNewMileage",
    "id",
    "price",
]
listings.drop(columns_to_drop, inplace=True, axis=1)

# columns that cannot be used for price prediction from 'feat_data' DataFrame
columns_to_drop = [
    "name_make",
    "name_model",
    "id_model",
    "name_engine",
    "equipmentType_engine",
    "code_engine",
    "availability_engine",
    "fuelType_engine",
    "totalValves_engine",
    "rpm.horsepower_engine",
    "rpm.torque_engine",
    "valve.timing_engine",
    "valve.gear_engine",
    "manufacturerEngineCode_engine",
    "equipmentType_transmission",
    "availability_transmission",
    "numOfDoors",
    "manufacturerCode",
    "baseMsrp_price",
    "baseInvoice_price",
    "deliveryCharges_price",
    "usedTmvRetail_price",
    "usedPrivateParty_price",
    "usedTradeIn_price",
    "estimateTmv_price",
    "tmvRecommendedRating_price",
    "primaryBodyType_categories",
    "vehicleSize_categories",
    "crossover_categories",
    "manufacturerCabType_categories",
    "squishVin",
    "matchingType",
    "displacement_engine",
    "status",
    "moreInfoUrl",
]
feat_data.drop(columns_to_drop, inplace=True, axis=1)

# keep most recent listings for cars showing up multiple times
dummy = listings.groupby(["vin"]).agg({"updatedAt": ["max"]}).reset_index()
dummy.columns = dummy.columns.droplevel(1)

listings = (
    listings.merge(dummy, how="inner", on=["vin", "updatedAt"])
    .drop_duplicates()
    .drop(["createdAt", "updatedAt"], axis=1)
)

# save cleaned data sets
listings.to_csv("CleanData/listings.csv", index=False)
feat_data.to_csv("CleanData/features.csv", index=False)

print(f"Listings data saved: Shape {listings.shape}")
print(f"Features data saved: Shape {feat_data.shape}")
