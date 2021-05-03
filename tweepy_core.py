from __future__ import unicode_literals
import tweepy
import os
import sys

HASH_TAGS_BY_LOCATION: dict = {
    "Bengaluru": [
        "#Bangalore ",
        "#BengaluruSOS ",
        "@BengaluruSOS ",
        "#CovidIndiaInfo ",
        "#Covid19IndiaHelp ",
        "#COVIDEmergency ",
        "#IndiaNeedsOxygen ",
    ],
    "Chennai": [
        "#Chennai ",
        "@104_GoTN ",
        "#BedsForTN ",
        "#CovidIndiaInfo ",
        "#Covid19IndiaHelp ",
        "#COVIDEmergency ",
        "#IndiaNeedsOxygen ",
    ],
    "Delhi": [
        "#Delhi ",
        "#CovidIndiaInfo ",
        "#Covid19IndiaHelp ",
        "#DelhiNCR ",
        "@dilipkpandey ",
        "@srinivasiyc ",
        "#COVIDEmergency ",
        "#IndiaNeedsOxygen ",
    ],
    "Mumbai": [
        "#Mumbai ",
        "#CovidIndiaInfo " "#Covid19IndiaHelp ",
        "#IndiaNeedsOxygen ",
    ],
    "Other": [
        "#CovidIndiaInfo " "#Covid19IndiaHelp ",
        "#IndiaNeedsOxygen ",
    ],
}
WILD_CARDS = [
    "patient_name",
    "patient_age",
    "location",
    "service_required",
    "current_spo2_level",
    "attendant_name",
    "attendant_contact_number",
    "plasma_service",
    "other_city",
]
TWEET_FORMAT: str = "Please extend help to:\nPatient Name: patient_name\nAge: patient_age\nLoc: location\nService Req: service_required\nSpO2: current_spo2_level\nAttendant Name: attendant_name\nContact#: attendant_contact_number\n"
TWEET_OTHER_CITY_DETAIL: str = " Other City: other_city"
TWEET_FOOTER = "**Automated using https://"


def get_env_var_from_os(env_var_name):
    env_var_val = None
    if env_var_name:
        raw_env_var_val = os.getenv(env_var_name)

        if raw_env_var_val:
            env_var_val = raw_env_var_val

    return env_var_val


def get_mandatory_env_variables():

    got_all_env_vars = False
    consumer_key = get_env_var_from_os("CONSUMER_KEY")
    print(consumer_key)
    consumer_secret = get_env_var_from_os("CONSUMER_SECRET")
    print(consumer_secret)

    access_token = get_env_var_from_os("ACCESS_TOKEN")
    print(access_token)
    access_token_secret = get_env_var_from_os("ACCESS_TOKEN_SECRET")
    print(access_token_secret)

    if None not in (consumer_key, consumer_secret, access_token, access_token_secret):
        got_all_env_vars = True

    return got_all_env_vars


def add_custom_hashtags_by_location(location: str):
    custom_tags_by_loc = "#HelpingIndiaBreathe "

    if location:
        hashtags_by_loc = HASH_TAGS_BY_LOCATION[location]
        for each_hashtag in hashtags_by_loc:
            custom_tags_by_loc += each_hashtag

    return custom_tags_by_loc


def post_a_tweet(info_to_tweet):
    tweet_post_url = None
    public_tweets = None

    got_all_env_vars = get_mandatory_env_variables()

    if got_all_env_vars is False:
        sys.exit(
            "Please set all mandatory Twitter Dev Acct Env Variables: CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET"
        )

    consumer_key = get_env_var_from_os("CONSUMER_KEY")
    consumer_secret = get_env_var_from_os("CONSUMER_SECRET")
    access_token = get_env_var_from_os("ACCESS_TOKEN")
    access_token_secret = get_env_var_from_os("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    tweet_to_post = TWEET_FORMAT
    loc_specific_info = None

    for each_wild_card in WILD_CARDS:

        if each_wild_card in info_to_tweet:
            tweet_to_post = tweet_to_post.replace(
                each_wild_card, str(info_to_tweet[each_wild_card])
            )

        if ("plasma_service" in info_to_tweet) and (each_wild_card == "plasma_service"):
            plasma_blood_group_chosen = str(info_to_tweet[each_wild_card])
            if plasma_blood_group_chosen:
                tweet_to_post += "Blood Group: " + plasma_blood_group_chosen + " \n"

        if ("location" in info_to_tweet) and (each_wild_card == "location"):
            location_chosen = str(info_to_tweet[each_wild_card])
            loc_specific_info = add_custom_hashtags_by_location(location_chosen)

    if loc_specific_info:
        tweet_to_post += loc_specific_info

    if ("other_city" in info_to_tweet) and (each_wild_card == "other_city"):
        tweet_to_post += TWEET_OTHER_CITY_DETAIL.replace(
            each_wild_card, str(info_to_tweet[each_wild_card])
        )

    tweet_to_post = str(tweet_to_post)
    print("Tweet length:" + str(len(tweet_to_post)))
    print("Tweet after replacing patient name and age:" + tweet_to_post)

    tweet_post_response = api.update_status(status=tweet_to_post)
    # print("type tweet_post_response: " + str(type(tweet_post_response)))
    # print("tweet_post_response: " + str(tweet_post_response))
    if tweet_post_response:
        tweet_post_json = tweet_post_response._json
        tweet_post_entities = tweet_post_json["entities"]
        tweet_post_urls = tweet_post_entities["urls"]
        tweet_post_url = tweet_post_urls[0]["url"]

    return tweet_post_url, tweet_to_post
    # return None, None


def get_all_tweets_by_hashtag(hash_tag_name: str):
    if hash_tag_name:
        return True
