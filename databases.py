from pymongo import MongoClient

class MongoDB:

    def __init__(self, host='localhost', port=27017, db='social_analytics', collection='tweets'):
        self.client = MongoClient(host, port)
        self.db = self.client[db]
        self.collection = self.db[collection]

    def add_tweet(self, status):
        self.collection.insert_one(status._json)
