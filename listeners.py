import sys
import os

from tweepy import StreamListener
from databases import MongoDB

from utils import get_full_text, is_retweet

class StdOutListener(StreamListener):
    
    def on_status(self, status):
        if not is_retweet(status):
            print(get_full_text(status))
            print('-' * 80)
        else:
            print(status._json['text'])

    def on_error(self, status_code):
        # apply built-in retry mechanism ("exponential backoff"),
        # to handle specific Twitter API errors
        # (https://developer.twitter.com/en/docs/basics/response-codes.html)
        
        if status_code in [420, 429]:
            return True
        
        return False

class MongoDBListener(StreamListener):

    def __init__(self, verbose=False, batch_size=100):
        super().__init__()
        self.driver = MongoDB(os.environ['MONGO_URL'])
        self.verbose = verbose

        # used for batching writes to MongoDB
        self.batch = []
        self.batch_size = batch_size
    
    def on_status(self, status):
        self.batch.append(status)
        
        # once the batch is large enough, dump batched tweets to MongoDB
        if len(self.batch) == self.batch_size:
            self.driver.add_tweets(self.batch)
            self.batch.clear()
        
        if self.verbose:
            if not is_retweet(status):
                print(get_full_text(status))
            else:
                print(status._json['text'])
            print('-' * 80)

    def on_error(self, status_code):
        # apply built-in retry mechanism ("exponential backoff"),
        # to handle specific Twitter API errors
        # (https://developer.twitter.com/en/docs/basics/response-codes.html)
        if status_code in [420, 429]:
            return True
        
        # make sure to save any batched tweets before shut-down
        if len(self.batch) > 0:
            self.driver.add_tweets(self.batch)
            self.batch.clear()
        
        return False

    def on_exception(self, exception):

        # make sure to save any batched tweets before shut-down
        if len(self.batch) > 0:
            self.driver.add_tweets(self.batch)
            self.batch.clear()
    
