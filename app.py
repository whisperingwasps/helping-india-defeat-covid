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
    plasma_service="",
    other_city="",
    other_city_chosen="None",
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
    ("Ask for Help", "Open-Source Project: Join hands", "Find Contacts", "Give help"),
)
if page_option == "Ask for Help":
    session_state.current_page_chosen = 0
elif page_option == "Find Contacts":
    session_state.current_page_chosen = 2
elif page_option == "Give help":
    session_state.current_page_chosen = 2
elif page_option == "Open-Source Project: Join hands":
    session_state.current_page_chosen = 1


st.sidebar.warning(
    "Disclaimer: Please note that the information on this page is crowdsourced and the maintainers of this site are not liable in case of any false information. Please also note that the maintainers or anyone claiming to be part of this site will not and do not ask for any financial help. This initiative is purely for charitable reasons. "
)


def contribute_page():
    st.header("Open-Source Project: Join hands")
    st.info(
        "This is an open source project based on Python programming language, so feel free to chip-in if you want to, at : [GitHub Repo](https://github.com/whisperingwasps/helping-india-defeat-covid)"
    )


def coming_soon_page():
    st.header("Stay Tuned...")
    st.warning("We are building this page. Stay tuned! ")


def ask_for_help_page():
    st.header("Ask for Help from India through Twitter")
    st.subheader("Submit Help Form")
    st.warning(
        "Please fill the below form and we will post a tweet in a format that tags the relevant volunteers and helps in faster response."
    )
    form = st.form(key="ask-help-for-COVID-form")

    with form:
        col1, mid, col2 = st.beta_columns([20, 1, 20])
        with col1:
            session_state.patient_name = st.text_input("Enter the patient name*")
            session_state.patient_age = st.number_input(
                "Enter the patient age*", min_value=18, max_value=150
            )
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
            session_state.plasma_service = st.selectbox(
                "If chosen Plasma, Select Blood Type*",
                [
                    "NA",
                    "Any",
                    "A+ve",
                    "A-ve",
                    "B+ve",
                    "B-ve",
                    "O+ve",
                    "O-ve",
                    "AB+ve",
                    "AB-ve",
                ],
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
            session_state.other_city = st.text_input(
                "If chosen Location as Other, Select Location/City name*"
            )

        submitted = st.form_submit_button("Post help on Twitter")

    if submitted:

        if len(session_state.contact_number) < 10:
            st.error("Attendant Contact Number is invalid. Please check and re-submit.")

        elif len(session_state.other_city) < 3:
            st.error("Please enter a valid city name")
        elif len(session_state.city) < 3:
            st.error("Please enter a valid city name")
        elif len(session_state.patient_name) < 3:
            st.error("Please enter a valid patiemt name")

        elif len(session_state.attendant_name) < 3:
            st.error("Please enter a valid attendant name.")

        elif (
            session_state.patient_name
            and session_state.patient_age
            and session_state.attendant_name
            and session_state.contact_number
            and session_state.spo2
            and session_state.city
            and session_state.service
            or session_state.plasma_service
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
                }

                if session_state.service == "Plasma":
                    tweet_info["plasma_service"] = session_state.plasma_service

                if session_state.city == "Other" and session_state.other_city:
                    tweet_info["other_city"] = session_state.other_city

                tweet_post_url, tweet_to_post = post_a_tweet(tweet_info)

                if tweet_post_url:
                    st.success(
                        "We have posted this [Tweet]("
                        + tweet_post_url
                        + ") on Twitter : "
                        + "  "
                        + tweet_to_post
                        + ".  "
                        + " Please follow the tweet on Twitter for updates."
                    )

        else:
            st.error("All the fields with * are mandatory.")


# Main Panel : Show Page chosen
available_pages = [ask_for_help_page, contribute_page, coming_soon_page]

page_turning_function = available_pages[session_state.current_page_chosen]
page_turning_function()
