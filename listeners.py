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

    def on_error(self, status_code):
        # apply built-in retry mechanism ("exponential backoff"),
        # to handle specific Twitter API errors
        # (https://developer.twitter.com/en/docs/basics/response-codes.html)
        
        if status_code in [420, 429]:
            return True
        
        return False

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

    def on_error(self, status_code):
        # apply built-in retry mechanism ("exponential backoff"),
        # to handle specific Twitter API errors
        # (https://developer.twitter.com/en/docs/basics/response-codes.html)
        
        if status_code in [420, 429]:
            return True
        
        return False
