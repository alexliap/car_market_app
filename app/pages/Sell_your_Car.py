import pandas as pd
import streamlit as st
from utils.price_prediction import get_pred

st.set_page_config(initial_sidebar_state="expanded")

st.title("Sell your Car")

st.markdown(
    "Here, you can add your car's features and get a recommendation on its sale price "
    "(*based on the market*) in case you want to sell it. "
    "**Make, Model and Year are mandatory to get a valuation.**"
)

tooltip_text = (
    "The suggestion you get is a rough estimate of the "
    "car's market worth, bacause the data used might "
    "not be enough."
)

col1, col2, col3 = st.columns(3)

price_prediction_data = pd.read_csv("app/data/PricePredictionData/data.csv")
mapping = pd.read_csv("app/data/Mapping/id_mapping.csv")

args_dict = {}

with col1:
    st.markdown("Main")

    select_make = st.selectbox("Select Make", mapping["make"].unique(), index=None)
    args_dict["make"] = select_make

    select_model = st.selectbox(
        "Select Model", mapping[mapping["make"] == select_make]["model"], index=None
    )
    try:
        args_dict["modelId"] = mapping[mapping["model"] == select_model][
            "modelId"
        ].item()
    except:
        pass

    select_year = st.selectbox("Select Year", range(1900, 2024), index=None)
    args_dict["year"] = select_year

    condition = st.selectbox(
        "New or Used",
        price_prediction_data["condition"].unique(),
        index=None,
    )
    args_dict["condition"] = condition

    fuel = st.selectbox(
        "Fuel type",
        price_prediction_data["type_engine"].unique(),
        index=None,
    )
    args_dict["fuel"] = fuel

if select_year and select_model and select_make:
    suggestion = st.button("Get Price", help=tooltip_text)
    if suggestion:
        pred, upper, lower = get_pred(price_prediction_data, **args_dict)

        st.write(f"Car should be placed at: " f"{pred-lower} \$ - {pred+upper} \$")

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

        bodyStyle = st.selectbox(
            "Car shape",
            price_prediction_data["bodyStyle"].unique(),
            index=None,
        )
        args_dict["bodyStyle"] = bodyStyle

    with col3:
        st.markdown("Miscellaneous")

        cylinders = st.selectbox(
            "Select number of cylinders",
            range(1, 17),
            index=None,
        )
        args_dict["cylinders"] = cylinders

        torque = st.number_input("Torque", value=None, placeholder="Torque...")
        args_dict["torque"] = torque

        configuration_engine = st.selectbox(
            "Engine shape",
            price_prediction_data["configuration_engine"].unique(),
            index=None,
        )
        args_dict["configuration_engine"] = configuration_engine

        market_categories = st.selectbox(
            "Market Category",
            price_prediction_data["market_categories"].unique(),
            index=None,
        )
        args_dict["market_categories"] = market_categories

        city_mpg = st.number_input(
            "City MPG", value=None, placeholder="Fuel Economy..."
        )
        args_dict["city_mpg"] = city_mpg

        highway_mpg = st.number_input(
            "Highway MPG", value=None, placeholder="Fuel Economy..."
        )
        args_dict["highway_mpg"] = highway_mpg


if select_make is not None and select_model is not None:
    make_model = " ".join([select_make, select_model])
