from tweepy import StreamListener
from pymongo import MongoClient

class StdOutListener(StreamListener):

    def on_status(self, status):

        print(status.text)

class MongoDBListener(StreamListener):

    pass
