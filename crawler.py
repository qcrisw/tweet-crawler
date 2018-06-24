import json
import sys
import os

import tweepy
import pymongo

from listeners import StdOutListener, MongoDBListener
from databases import MongoDB

class TweetCrawler:
    
    def __init__(self, auth):
        self.auth = auth
        self.api = tweepy.API(auth)
        self.db = MongoDB()

    def crawl_tweets(self, tracks=None):
        '''Implements the core logic for crawling a stream of tweets.'''
        
        # initialize a stream object to connect with Twitter's Streaming API
        main_listener = MongoDBListener(verbose=True)
        main_stream = tweepy.Stream(auth=self.auth, listener=main_listener)
        
        # raise an exception if no track was specified
        if tracks is None or len(tracks) == 0:
            raise RuntimeError('You MUST specify at least one streaming track')
        
        main_stream.filter(track=tracks)

def main():
    # retrieve the crawler's configuration options
    config = {
        "consumer_key": os.environ['TWITTER_CONSUMER_KEY'],
        "consumer_secret": os.environ['TWITTER_CONSUMER_SECRET'],
        "access_token": os.environ['TWITTER_ACCESS_TOKEN'],
        "access_token_secret": os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    }

    # TODO raise exception if any of the above are not defined
    # TODO encapsulate config json in a new config.py

    # authenticate the crawler to access the Twitter API
    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])

    # create and run the tweet crawler
    crawler = TweetCrawler(auth)
    filter = sys.argv[1:]
    print("Listening for Twitter stream on '{}'...".format(filter))
    sys.stdout.flush()
    crawler.crawl_tweets(filter)

if __name__ == '__main__':
    main()
