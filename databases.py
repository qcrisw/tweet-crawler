from pymongo import MongoClient

class MongoDB:

    def __init__(self, url='mongodb://localhost:27017/social_analytics'):
        self.client = MongoClient(url)
        db = self.client.get_database()
        self.collection = db['tweets']

    def add_tweet(self, status):
        self.collection.insert_one(status._json)
