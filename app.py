import streamlit as st
import SessionState
from tweepy_core import post_a_tweet, get_mandatory_env_variables
import sys

session_state = SessionState.get(
    current_page_chosen=0,
    patient_name="",
    patient_age="",
    attendant_name="",
    contact_number="",
    spo2="",
    city="",
    service="",
    other_city="",
)

got_all_env_vars = get_mandatory_env_variables()
print("got_all_env_vars: " + str(got_all_env_vars))

if got_all_env_vars is False:
    sys.exit(
        "Please set all mandatory Twitter Dev Acct Env Variables: CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET"
    )

st.set_page_config(
    page_title="Helping India Fight COVID", layout="wide", initial_sidebar_state="auto"
)
st.sidebar.header("Helping India Defeat COVID")
st.sidebar.info(
    "A non profit and volunteer initiative, based on crowdsourced data trying to help Indians with the resources needed to defeat COVID-19"
)
#####Side-bar NAV BAR:
st.sidebar.markdown(" ### Navigation")
st.sidebar.markdown("Choose a page to proceed:")
page_option = st.sidebar.radio(
    "What do you want us to help you with?",
    ("Ask for Help", "Find Contacts", "Give help"),
)
if page_option == "Ask for Help":
    session_state.current_page_chosen = 0
elif page_option == "Find Contacts":
    session_state.current_page_chosen = 1
elif page_option == "Give help":
    session_state.current_page_chosen = 1


def coming_soon_page():
    st.header("Stay Tuned...")
    st.warning("We are building this page. Stay tuned! ")


def ask_for_help_page():
    st.header("Ask for Help from India")
    st.subheader("Submit Help Form")
    st.warning(
        "Please fill the below form and we will post a tweet in a format that tags the relevant volunteers and helps in faster response."
    )
    form = st.form(key="ask-help-for-COVID-form")

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

        submitted = st.form_submit_button("Post help on Twitter")

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
                        + ") on Twitter : "
                        + "\n"
                        + tweet_to_post
                        + ". \n"
                        + " Please follow the tweet on Twitter for updates."
                    )

        else:
            st.error("All the fields with * are mandatory.")


# Main Panel : Show Page chosen
available_pages = [ask_for_help_page, coming_soon_page]

page_turning_function = available_pages[session_state.current_page_chosen]
page_turning_function()
