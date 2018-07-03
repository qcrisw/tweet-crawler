from pymongo import MongoClient

from utils import expand_tweet

class MongoDB:

    def __init__(self, url='mongodb://localhost:27017/social_analytics'):
        self.client = MongoClient(url)
        db = self.client.get_database()
        self.collection = db['tweets']

    def add_tweet(self, status):
        # expand text of tweet to retrieve full tweet body
        expand_tweet(status)
        self.collection.insert_one(status._json)

    def add_tweets(self, tweets):
        # expand each tweet and store its JSON in MongoDB
        tweet_json = []
        
        for tweet in tweets:
            expand_tweet(tweet)
            tweet_json.append(tweet._json)

        self.collection.insert_many(tweet_json, ordered=False)
