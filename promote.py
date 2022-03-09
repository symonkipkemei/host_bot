import tweepy
import logging
from config import create_api
import json
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
                tweet.user.id == self.me.id:
            # This tweet is a reply or I'm it's author so, ignore it
            return

        if not tweet.retweeted:
            try:
                tweet.retweet()
                time.sleep(36)
                print("Symon, waiting for 36 secs")

            except Exception as e:
                logger.error("Error on retweet", exc_info=True)

    def on_error(self, status):
        logger.error(status)


def main(keywords):
    api = create_api()
    tweets_Listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_Listener)
    stream.filter(track=keywords, languages=["en"])


if __name__ == "__main__":
    main(["#nodejs", "#python"])
