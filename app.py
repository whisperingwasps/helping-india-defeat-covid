import streamlit as st
import SessionState
from tweepy_core import post_a_tweet

st.sidebar.header("Helping India Defeat COVID")
st.sidebar.info(
    "A non profit and volunteer initiative, based on crowdsourced data trying to help Indians with the resources needed to defeat COVID-19"
)
st.warning(
    "Please fill the below form and we will post a tweet in a format that tags the relevant volunteers and helps in faster response."
)
form = st.form(key="my-form")
session_state = SessionState.get(
    patient_name="",
    patient_age="",
    attendant_name="",
    contact_number="",
    spo2="",
    city="",
    service="",
    other_city="",
)
with form:
    col1, mid, col2 = st.beta_columns([20, 1, 20])
    with col1:
        session_state.patient_name = st.text_input("Enter the patient name*")
        session_state.patient_age = st.text_input("Enter the patient age*")
        session_state.service = st.selectbox(
            "Select service*",
            [
                "ICU Beds",
                "Ventilator",
                "Plasma",
                "Medicines",
                "Food Home Delivery",
                "Ambulance",
            ],
            key=1,
        )
        session_state.address = st.text_input("Enter the address*")
    with col2:
        session_state.attendant_name = st.text_input("Enter the attendant name*")
        session_state.contact_number = st.text_input(
            "Enter the attendant contact number*"
        )
        session_state.city = st.selectbox(
            "Select City*", ["Delhi", "Mumbai", "Chennai", "Bengaluru", "Other"], key=2
        )

        session_state.spo2 = st.selectbox(
            f"Enter the current SPO2 Level",
            [
                "Below 60",
                "Betweeen 60 to 70",
                "Between 70 to 80",
                "Between 80 to 90",
            ],
            key="spo2",
        )

    submitted = st.form_submit_button("Submit")


if submitted:
    if session_state.city == "Other":
        session_state.other_city = st.text_input("Enter the city*")
    if (
        session_state.patient_name
        and session_state.patient_age
        and session_state.attendant_name
        and session_state.contact_number
        and session_state.spo2
        and session_state.city
        and session_state.service
        and session_state.address
    ):
        with st.spinner("Posting a tweet"):
            public_tweets = post_a_tweet()
            for each_tweet in public_tweets:
                st.success("Tweet is : " + str(each_tweet))

    else:
        st.error("All the fields with * are mandatory.")
