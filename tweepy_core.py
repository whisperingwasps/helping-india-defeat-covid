import tweepy
import os

WILD_CARDS = [
    "patient_name",
    "patient_age",
    "location",
    "service_required",
    "current_spo2_level",
    "attendant_name",
    "attendant_contact_number",
    "address",
]
TWEET_FORMAT = "Patient Name: patient_name\nPatient age: patient_age\nLocation: location\nService Required: service_required\nCurrent SpO2: current_spo2_level\nAttendant Name: attendant_name\nContact Number: attendant_contact_number\nAddress: address\n#HelpingIndiaBreathe\n**Automated using https://"


def post_a_tweet(info_to_tweet):
    tweet_post_url = None
    public_tweets = None
    consumer_key = os.getenv("CONSUMER_KEY")
    print(consumer_key)
    consumer_secret = os.getenv("CONSUMER_SECRET")
    print(consumer_secret)

    access_token = os.getenv("ACCESS_TOKEN")
    print(access_token)
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
    print(access_token_secret)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    tweet_to_post = TWEET_FORMAT

    for each_wild_card in WILD_CARDS:
        tweet_to_post = tweet_to_post.replace(
            each_wild_card, info_to_tweet[each_wild_card]
        )

    """tweet_patient_name = TWEET_FORMAT.replace(
        "<PATIENT_NAME>", info_to_tweet["patient_name"]
    )
    tweet_patient_age = tweet_patient_name.replace(
        "<PATIENT_AGE>", info_to_tweet["patient_age"]
    )"""

    print("Tweet after replacing patient name and age:" + str(tweet_to_post))

    tweet_post_response = api.update_status(status=tweet_to_post)
    print("type tweet_post_response: " + str(type(tweet_post_response)))
    print("tweet_post_response: " + str(tweet_post_response))
    if tweet_post_response:
        tweet_post_json = tweet_post_response._json
        tweet_post_entities = tweet_post_json["entities"]
        tweet_post_urls = tweet_post_entities["urls"]
        tweet_post_url = tweet_post_urls[0]["url"]

    """public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)"""

    return tweet_post_url, tweet_to_post
