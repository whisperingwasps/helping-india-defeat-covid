import tweepy
import os


def post_a_tweet():
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

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)

    return public_tweets
