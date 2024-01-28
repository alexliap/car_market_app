import pandas as pd
import streamlit as st

mapping = pd.read_csv("app/data/Mapping/id_mapping.csv")

st.session_state.disabled = True

st.set_page_config(initial_sidebar_state="expanded")

st.title("Car Recommender")

st.markdown(
    "Here, you can car recommendation with respect to the car you insert."
    "Depending on the car you will get up to 5 recommended cars back that are similar to the one entered."
)

select_make = st.selectbox("Select Make", mapping["make"].unique(), index=None)

select_model = st.selectbox(
    "Select Model", mapping[mapping["make"] == select_make]["model"], index=None
)
