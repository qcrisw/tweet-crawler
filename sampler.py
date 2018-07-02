from urllib3.exceptions import ProtocolError

import tweepy

from listeners import StdOutListener
from databases import MongoDB
from config import config

# "random sample" tweet crawler
class TweetSampler:

    def __init__(self, auth):
        self.auth = auth
        self.api = tweepy.API(auth)
        self.db = MongoDB()

    def crawl_tweets(self):
        
        main_listener = StdOutListener()
        
        while True:
            
            try:
                main_stream = tweepy.Stream(auth=self.auth, listener=main_listener)

                # start crawling a random sample of *all* tweets (BLOCKING call!)
                main_stream.sample()

            except ProtocolError:
                #print('\nSampler thread is stalling! Starting new tweet sampler...\n')
                continue

# driver for "random sample" crawler
def main():
    # authenticate the crawler to access the Twitter API
    auth = tweepy.OAuthHandler(config['consumer_key'],
                               config['consumer_secret'])

    auth.set_access_token(config['access_token'],
                          config['access_token_secret'])

    # create and run the tweet sampler
    sampler = TweetSampler(auth)
    print('Listening for random sample of tweets...', flush=True)

    # gracefully handle Ctrl^C exit from tweet sampling process
    try:
        sampler.crawl_tweets()
    except KeyboardInterrupt:
        print('\nStopped tweet sampler...')
        
if __name__ == '__main__':

    main()
