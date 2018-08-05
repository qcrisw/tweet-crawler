import sys
import os

from tweepy import StreamListener

from databases import MongoDB
from mq.task_queue import TaskQueue
from mq.tasks import mongo_add_tweets
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

class DBListener(StreamListener):

    def __init__(self, driver, verbose=False, batch_size=100):
        super().__init__()
        self.driver = driver
        self.verbose = verbose
        
        # used for batching writes to database
        self.batch = []
        self.batch_size = batch_size
        
        # job queue for post-crawling tasks (i.e. db write, annotation, etc.)
        self.q = TaskQueue('crawler_out', url=os.environ['REDIS_URL'])
    
    def on_status(self, status):
        self.batch.append(status)
        
        # once the batch is large enough, dump batched tweets
        # to database via an intermediate job queue
        if len(self.batch) == self.batch_size:
            self.q.add_task(mongo_add_tweets, self.batch)
            self.batch = []
        
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
            self.q.add_task(mongo_add_tweets, self.batch)
            self.batch = []
        
        return False

    def on_exception(self, exception):
        
        # make sure to save any batched tweets before shut-down
        if len(self.batch) > 0:
            self.q.add_task(mongo_add_tweets, self.batch)
            self.batch = []

class MongoDBListener(DBListener):

    def __init__(self, verbose=False, batch_size=100):
        super().__init__(MongoDB(os.environ['MONGO_URL']), verbose, batch_size)
