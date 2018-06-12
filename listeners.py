import sys

from tweepy import StreamListener
from databases import MongoDB

from utils import get_full_text

class StdOutListener(StreamListener):
    
    def on_status(self, status):
        print(get_full_text(status))
        print('-' * 80)

class MongoDBListener(StreamListener):

    def __init__(self):
        super().__init__()
        self.driver = MongoDB()

    def on_status(self, status):
        self.driver.add_tweet(status)
