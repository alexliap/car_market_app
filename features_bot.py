import os

import numpy as np
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from key import pick_key

api_key = pick_key()

# get listings data
data = pd.read_csv("RawData/data.csv")

# get unique vin numbers
vin_list = np.unique(data["vin"].values).tolist()

# check if there is already a features dataset
if os.path.isfile("RawData/features_data.csv"):
    ft_data = pd.read_csv("RawData/features_data.csv")
else:
    ft_data = pd.DataFrame(columns=["vin"])

# loop over all vin numbers to get their features
for vin in vin_list:
    try:
        # check if there are already features for this vin number
        if vin not in ft_data["vin"].values:
            url = f"https://auto.dev/api/vin/{vin}?apikey={api_key}"

            session = requests.Session()
            retry = Retry(connect=3, backoff_factor=1)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            response = session.get(url)
            data = pd.DataFrame()
            data["vin"] = [vin]
            for item in response.json().keys():
                if item not in ["options", "years", "colors"]:
                    # some keys from the response are dicts themselves so we dig a level deeper
                    if isinstance(response.json()[item], dict):
                        data = pd.concat(
                            [
                                data,
                                pd.json_normalize(response.json()[item]).add_suffix(
                                    "_" + item
                                ),
                            ],
                            axis=1,
                        )
                    else:
                        data[item] = response.json()[item]

            ft_data = pd.concat([ft_data, data], axis=0)
            print(ft_data.shape)
            # we overwrite the file at the end of every iteration in case something goes wrong
            ft_data.to_csv("RawData/features_data.csv", index=False)
    except:
        pass
