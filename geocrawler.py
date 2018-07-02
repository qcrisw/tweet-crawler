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

    def crawl_tweets(self, tracks=None):
        '''Implements the core logic for crawling a stream of tweets.'''
        
        # initialize a stream object to connect with Twitter's Streaming API
        main_listener = MongoDBListener(verbose=True)
        
        # raise an exception if no track was specified
        if tracks is None or len(tracks) == 0:
            raise RuntimeError('You MUST specify at least one streaming track')

        # automatically re-connect tweet crawler whenever it stalls
        while True:
            try:
                # open up a SYNCHRONOUS connection to Twitter Streaming API
                main_stream = tweepy.Stream(auth=self.auth,
                                            listener=main_listener)
                main_stream.filter(track=tracks)
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
    filter = sys.argv[1:]
    print("Listening for Twitter stream on '{}'...".format(filter))
    sys.stdout.flush()

    # gracefully handle Ctrl^C exit from tweet crawling process
    try:
        crawler.crawl_tweets(filter)
    except KeyboardInterrupt:
        print('\nStopped tweet crawler for tracks: {}'.format(filter))

if __name__ == '__main__':
    main()
