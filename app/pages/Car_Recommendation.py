import pandas as pd
import streamlit as st
from utils.clustering import get_car_representation, get_recommendation, get_scores

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

if select_make is not None and select_model is not None:
    make_model = " ".join([select_make, select_model])
    # get car representation array
    car_representation = get_car_representation(make_model)
    # get scores
    scores = get_scores(make_model, car_representation)
    # get recommendations
    recs = get_recommendation(make_model, scores)

    if len(recs) != 0:
        for item in recs:
            st.markdown("- " + item)
    else:
        st.markdown("Oh maaaaan, a car like no other!")
