from tweepy import StreamListener
from databases import MongoDB

class StdOutListener(StreamListener):

    def on_status(self, status):
        print(status.text)

class MongoDBListener(StreamListener):

    def __init__(self):
        super().__init__()
        self.driver = MongoDB()

    def on_status(self, status):
        self.driver.add_tweet(status)
