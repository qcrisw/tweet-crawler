from urllib3.exceptions import ProtocolError
import sys

import tweepy

from listeners import StdOutListener, MongoDBListener
from databases import MongoDB
from config import config

# "random sample" tweet crawler
class TweetSampler:

    def __init__(self, auth):
        self.auth = auth
        self.api = tweepy.API(auth)
        self.db = MongoDB()

    def crawl_tweets(self, languages=None):
        
        main_listener = MongoDBListener(verbose=True)
        languages = languages or []
        
        while True:
            
            try:
                # create a stream object to connect with Twitter's Streaming API
                main_stream = tweepy.Stream(auth=self.auth, listener=main_listener)

                # connect to an IP proxy, if specified in the environment
                proxy_ip = config.get('proxy_server')
                if proxy_ip:
                    main_stream.proxies = {
                        'http': proxy_ip,
                        'https': proxy_ip
                    }

                # start crawling all tweets in the given language(s)
                # NOTE: This is a BLOCKING call!
                main_stream.sample(languages=languages)

            except ProtocolError:
                continue

# driver for "random sample" crawler
def main():
    # authenticate the crawler to access the Twitter API
    auth = tweepy.OAuthHandler(config['consumer_key'],
                               config['consumer_secret'])

    auth.set_access_token(config['access_token'],
                          config['access_token_secret'])

    # create and run the tweet sampler for the given languages
    sampler = TweetSampler(auth)
    langs = sys.argv[1:]
    print('Using proxy server at {}'.format(config.get('proxy_server')))
    print('Listening for random sample of tweets in languages: {}'.format(langs), flush=True)

    # gracefully handle Ctrl^C exit from tweet sampling process
    try:
        sampler.crawl_tweets(languages=langs)
    except KeyboardInterrupt:
        print('\nStopped tweet sampler for tweets in languages: {}'.format(langs))
        
if __name__ == '__main__':

    main()
