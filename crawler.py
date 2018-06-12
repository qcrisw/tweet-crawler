import json

import tweepy
import pymongo

from listeners import StdOutListener, MongoDBListener
from databases import MongoDB

class TweetCrawler:
    def __init__(self):
        self.db = MongoDB()
        pass

    def crawl_tweets(self):
        pass

def main():
    crawler = TweetCrawler()
    crawler.crawl_tweets()

if __name__ == '__main__':
    main()
