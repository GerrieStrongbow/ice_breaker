import os
from dotenv import load_dotenv
import tweepy
import requests

load_dotenv()

twitter_client = tweepy.Client(
    bearer_token=os.environ.get("TWITTER_BEARER_TOKEN"),
    consumer_key=os.environ.get("TWITTER_API_KEY"),
    consumer_secret=os.environ.get("TWITTER_API_KEY_SECRET"),
    access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"),
)


def scrape_user_tweets(username: str, num_tweets: int = 5, mock: bool = False) -> list:
    """
    Scrapes a Twitter user's original tweets (i.e., not retweets) and return them as a list of disctionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url".
    """

    tweet_list = []

    if mock:
        EDEN_TWITTER_GIST = "https://gist.githubusercontent.com/emarco177/9d4fdd52dc432c72937c6e383dd1c7cc/raw/1675c4b1595ec0ddd8208544a4f915769465ed6a/eden-marco-tweets.json"
        tweets = requests.get(EDEN_TWITTER_GIST, timeout=5).json()

    else:
        user_id = twitter_client.get_user(username=username).data.id
        tweets = twitter_client.get_users_tweets(
            id=user_id,
            max_results=num_tweets,
            exclude=["replies", "retweets"],
        ).data

    for tweet in tweets:
        tweet_dict = {}
        tweet_dict["text"] = tweet["text"]
        tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet['id']}"
        tweet_list.append(tweet_dict)

    return tweet_list


if __name__ == "__main__":

    tweets = scrape_user_tweets(username="EdenEmarco177", mock=True)
    print(tweets)
