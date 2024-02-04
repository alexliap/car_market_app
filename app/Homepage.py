import pandas as pd
import plotly.express as px
import streamlit as st
from utils.plots import brand_pie_chart

st.set_page_config(initial_sidebar_state="expanded")

st.title("Homepage")

st.markdown(
    "This is a demo app for the ML course of MSc Program in AI by University of Piraeus and NCSR Demokritos. "
    "For this project, car listing data was collected along with vehicle features for the corresponding VIN numbers. "
    "In the homepage, the user can see various stats about the data collected.\n\n"
    "Two extra features of the demo app are:\n"
    "- Price Recommendation, where the user gets a suggestion of how he should price his car.\n"
    "- Car Recommendation, where the user inputs a car and gets recommended with up to five similar cars.\n\n"
    "In this page, you can see some descreptive stuff about the datasets used."
)

price_prediction_data = pd.read_csv("app/data/PricePredictionData/data.csv")
# price histogram
price_hist = px.histogram(
    price_prediction_data,
    x="priceUnformatted",
    nbins=100,
    title="Price Distribution",
    labels={"priceUnformatted": "Price in $"},
).update_layout(yaxis_title="Counts")
st.plotly_chart(price_hist, use_container_width=True)

# brand freq chart
brand_pie_chart = brand_pie_chart(price_prediction_data)
st.plotly_chart(brand_pie_chart, use_container_width=True)
