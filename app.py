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
            "Select City/Location*",
            ["Delhi", "Mumbai", "Chennai", "Bengaluru", "Other"],
            key=2,
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
            tweet_info = {
                "patient_name": session_state.patient_name,
                "patient_age": session_state.patient_age,
                "location": session_state.city,
                "service_required": session_state.service,
                "current_spo2_level": session_state.spo2,
                "attendant_name": session_state.attendant_name,
                "attendant_contact_number": session_state.contact_number,
                "address": session_state.address,
            }
            if session_state.city == "Other":
                tweet_info["city"] = session_state.other_city

            tweet_post_url, tweet_to_post = post_a_tweet(tweet_info)

            if tweet_post_url:
                st.success(
                    "We have posted this [Tweet]("
                    + tweet_post_url
                    + ") on Twitter : \n  "
                    + tweet_to_post
                    + ". \n"
                    + " Please follow the tweet on Twitter for updates."
                )

    else:
        st.error("All the fields with * are mandatory.")
