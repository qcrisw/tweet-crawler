from pymongo import MongoClient
from pymongo.errors import BulkWriteError

from utils import expand_tweet, reformat_tweet

class MongoDB:

    def __init__(self, url='mongodb://localhost:27017/social_analytics'):
        self.client = MongoClient(url)
        db = self.client.get_database()
        self.collection = db['tweets']

    def add_tweet(self, status):
        # add "full_tweet" field to status object
        expand_tweet(status)
        # convert raw date-string fields into datetime objects
        reformat_tweet(status)
        self.collection.insert_one(status._json)

    def add_tweets(self, tweets):
        # add "full_tweet" field to each tweet object
        # and store its JSON in MongoDB
        # 
        # Also, convert the raw "date strings" sent by
        # the Twitter API into actual datetime objects
        tweet_json = []
        
        for tweet in tweets:
            expand_tweet(tweet)
            reformat_tweet(tweet)
            tweet_json.append(tweet._json)
        
        # try to insert each tweet contained in tweet_json into MongoDB
        # Note: Any attempt to insert duplicate tweet IDs is ignored
        try:
            self.collection.insert_many(tweet_json, ordered=False)
        except BulkWriteError:
            pass
