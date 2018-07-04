import json
import sys
from urllib3.exceptions import ProtocolError

import tweepy
import pymongo

from listeners import StdOutListener, MongoDBListener
from databases import MongoDB
from config import config

class TweetCrawler:
    
    def __init__(self, auth):
        self.auth = auth
        self.api = tweepy.API(auth)
        self.db = MongoDB()

    def crawl_tweets(self, locations=None):
        '''Implements the core logic for crawling a stream of tweets.'''
        
        # create a listener to consume tweets from Twitter's Streaming API
        main_listener = MongoDBListener(verbose=True)
        
        # raise an exception if no track was specified
        if locations is None or len(locations) == 0:
            raise RuntimeError('You MUST specify at least one valid bounding box')

        # automatically re-connect tweet crawler whenever it stalls
        while True:
            try:
                # open up a SYNCHRONOUS connection to Twitter Streaming API
                main_stream = tweepy.Stream(auth=self.auth,
                                            listener=main_listener)
                main_stream.filter(locations=locations)
            except ProtocolError:
                # the client is beginning to stall, so re-connect it
                continue

def main():
    # authenticate the crawler to access the Twitter API
    auth = tweepy.OAuthHandler(config['consumer_key'],
                               config['consumer_secret'])
    
    auth.set_access_token(config['access_token'],
                          config['access_token_secret'])

    # create and run the tweet crawler
    crawler = TweetCrawler(auth)
    locations = list(map(float, sys.argv[1:]))
    print("Listening for Tweets within bounding box: {}...".format(locations))
    sys.stdout.flush()

    # gracefully handle Ctrl^C exit from tweet crawling process
    try:
        crawler.crawl_tweets(locations)
    except KeyboardInterrupt:
        print('\nStopped tweet crawler for bounding box: {}'.format(locations))

if __name__ == '__main__':
    main()
