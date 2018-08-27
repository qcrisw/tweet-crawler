import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from utils import expand_tweet, reformat_tweet
from utils import expand_hashtags, expand_mentions
from utils import get_collection_name, get_mongo_lang_code

class MongoDB:

    def __init__(self, url='mongodb://localhost:27017/social_analytics'):
        self.client = MongoClient(url)
        self.db = self.client.get_database()
        self.collection = self.db['tweets']

    def add_tweet(self, status):
        # add "full_tweet" field to status object
        expand_tweet(status)
        # convert raw date-string fields into datetime.datetime objects
        reformat_tweet(status)
        # expose top-level hashtags via "full_hashtags" field
        expand_hashtags(status)
        # expose top-level user mentions via "full_mentions" field
        expand_mentions(status)
        
        # select appropriate daily collection based on tweet creation time
        self.collection = self.db[get_collection_name(status)]
        
        # if this is an unindexed collection, create the following:
        #   - text index on .full_text
        #   - multikey index on .full_hashtags.text
        #   - multikey index on .full_mentions.screen_name
        if 'full_tweet_text' not in self.collection.index_information():
            self.collection.create_index([('full_tweet', pymongo.TEXT)],
                                         language_override='index_lang',
                                         default_language='en')
            self.collection.create_index('full_hashtags.text')
            self.collection.create_index('full_mentions.screen_name')
            
        # set primary key (_id) to Tweet ID sent by Twitter API
        status._json['_id'] = status._json['id_str']
        
        # set .index_lang for mongo text indexing
        status._json['index_lang'] = get_mongo_lang_code(status._json['lang'])
        
        # insert tweet into daily collection, while ignoring duplicates
        try:
            self.collection.insert_one(status._json)
        except DuplicateKeyError:
            pass

    def add_tweets(self, tweets):
        '''sequentially insert a list of Status objects into MongoDB'''
        for tweet in tweets:
            self.add_tweet(tweet)
