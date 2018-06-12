import json

import tweepy
import pymongo

from listeners import StdOutListener, MongoDBListener
from databases import MongoDB

class TweetCrawler:
    
    def __init__(self, auth):
        self.auth = auth
        self.api = tweepy.API(auth)
        self.db = MongoDB()

    def crawl_tweets(self):
        pass

def main():
    # retrieve the crawler's configuration options
    with open('config.json') as f:
        config = json.load(f)

    # authenticate the crawler to access the Twitter API
    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])

    # create and run the tweet crawler
    crawler = TweetCrawler(auth)
    crawler.crawl_tweets()

if __name__ == '__main__':
    main()
