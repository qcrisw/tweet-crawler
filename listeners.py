import sys
import os

from tweepy import StreamListener
from databases import MongoDB

from utils import get_full_text, is_retweet

class StdOutListener(StreamListener):
    
    def on_status(self, status):
        if (not is_retweet(status)):
            print(get_full_text(status))
            print('-' * 80)

class MongoDBListener(StreamListener):

    def __init__(self, verbose=False):
        super().__init__()
        self.driver = MongoDB(os.environ['MONGO_URL'])
        self.verbose = verbose
    
    def on_status(self, status):
        if not is_retweet(status):
            self.driver.add_tweet(status)
            
            if self.verbose:
                print(get_full_text(status))
                print('-' * 80)
    
