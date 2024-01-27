import os

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from key import pick_key

api_key = pick_key()
url = f"https://auto.dev/api/listings?apikey={api_key}&page="

amount_of_pg = 250

if os.path.isfile("RawData/data.csv"):
    data = pd.read_csv("RawData/data.csv")
else:
    data = pd.DataFrame()

for i in range(1, amount_of_pg):
    try:
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.8)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        response = session.get(url + str(i))
        response_data = pd.json_normalize(response.json()["records"])
        response_data = response_data[
            [
                "id",
                "vin",
                "displayColor",
                "year",
                "make",
                "model",
                "price",
                "mileage",
                "city",
                "lat",
                "lon",
                "condition",
                "modelId",
                "active",
                "state",
                "trim",
                "bodyType",
                "bodyStyle",
                "regionName",
                "experience",
                "mileageUnformatted",
                "mileageHumanized",
                "priceMobile",
                "priceUnformatted",
                "recentPriceDrop",
                "showNewMileage",
                "eligibleForFinancing",
                "financingExperience",
                "isHot",
                "monthlyPayment",
                "newPriceAsMsrp",
                "createdAt",
                "updatedAt",
            ]
        ]
        data = pd.concat([data, response_data], axis=0)
        data = data.drop_duplicates()
        print(data.shape)
        data.to_csv("RawData/data.csv", index=False)
    except:
        print("Somehting happened!")
