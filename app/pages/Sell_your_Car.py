import pandas as pd
import streamlit as st
from utils.price_prediction import get_pred

st.set_page_config(initial_sidebar_state="expanded")

st.title("Sell your Car")

col1, col2, col3 = st.columns(3)

price_prediction_data = pd.read_csv("app/data/PricePredictionData/data.csv")
mapping = pd.read_csv("app/data/Mapping/id_mapping.csv")

args_dict = {}

with col1:
    st.markdown("Mandatory")

    select_make = st.selectbox("Select Make", mapping["make"].unique(), index=None)
    args_dict["make"] = select_make

    select_model = st.selectbox(
        "Select Model", mapping[mapping["make"] == select_make]["model"], index=None
    )
    args_dict["modelId"] = mapping[mapping["model"] == select_model]["modelId"].item()

    select_year = st.selectbox("Select Year", range(1900, 2024), index=None)
    args_dict["year"] = select_year

if select_year and select_model and select_make:
    with col2:
        st.markdown("Extra")

        mileage = st.number_input("Mileage", value=None, placeholder="Car Mileage...")
        args_dict["mileage"] = mileage

        transmission = st.selectbox(
            "Select Transmission Type",
            price_prediction_data["name_transmission"].unique(),
            index=None,
        )
        print(transmission)
        args_dict["transmission"] = transmission

        displacement = st.number_input(
            "Displacement(L)", value=None, placeholder="Car Displacement..."
        )
        args_dict["displacement"] = displacement

        hp = st.number_input("Horsepower", value=None, placeholder="Car Horsepower...")
        args_dict["hp"] = hp

        drivenWheels = st.selectbox(
            "Select Drive Type",
            price_prediction_data["drivenWheels"].unique(),
            index=None,
        )
        args_dict["drivenWheels"] = drivenWheels

        tooltip_text = (
            "The suggestion you get is a rough estimate of the "
            "car's market worth, bacause the data used might "
            "not be enough."
        )
        suggestion = st.button("Get Price", help=tooltip_text)
        if suggestion:
            get_pred(price_prediction_data, **args_dict)

    with col3:
        st.markdown("Miscellaneous")


if select_make is not None and select_model is not None:
    make_model = " ".join([select_make, select_model])
