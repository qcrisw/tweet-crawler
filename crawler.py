import json
import sys

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
        
        # start tracking tweets containing the requested terms, if any
        tracks = tracks or ['python']
        main_stream.filter(track=tracks)

def main():
    # retrieve the crawler's configuration options
    with open('config.json') as f:
        config = json.load(f)

    # authenticate the crawler to access the Twitter API
    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])

    # create and run the tweet crawler
    crawler = TweetCrawler(auth)
    crawler.crawl_tweets(sys.argv[1:])

if __name__ == '__main__':
    main()
