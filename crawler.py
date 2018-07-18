import sys
from urllib3.exceptions import ProtocolError

import tweepy

from listeners import StdOutListener, MongoDBListener
from databases import MongoDB
from config import config

class TweetCrawler:
    
    def __init__(self, auth):
        self.auth = auth
        self.api = tweepy.API(auth)
        self.db = MongoDB()

    def crawl_geolocations(self, locations=None):
        '''Implements the core logic for crawling a stream of tweets.'''
        
        # create a listener to consume tweets from Twitter's Streaming API
        main_listener = MongoDBListener(verbose=True)
        
        # raise an exception if no locations were specified
        if locations is None or len(locations) == 0:
            raise RuntimeError('You MUST specify at least one valid bounding box')
        
        # automatically re-connect tweet crawler whenever it stalls
        while True:
            try:
                # open up a SYNCHRONOUS connection to Twitter Streaming API
                main_stream = tweepy.Stream(auth=self.auth,
                                            listener=main_listener)
                
                # connect to an IP proxy, if specified in the environment
                proxy_ip = config.get('proxy_server')
                if proxy_ip:
                    main_stream.proxies = {
                        'http': proxy_ip,
                        'https': proxy_ip
                    }
                    
                # start up the "filter" streaming crawler
                main_stream.filter(locations=locations)
                    
            except ProtocolError:
                # the client is beginning to stall, so re-connect it
                continue
            
    def crawl_tracks(self, tracks=None):
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

                # connect to an IP proxy, if specified in the environment
                proxy_ip = config.get('proxy_server')
                if proxy_ip:
                    main_stream.proxies = {
                        'http': proxy_ip,
                        'https': proxy_ip
                    }
                    
                # start up the "filter" streaming crawler
                main_stream.filter(track=tracks)
            except ProtocolError:
                # the client is beginning to stall, so re-connect it
                continue

    def crawl_sample(self, languages=None):
    
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

def main():
    # authenticate the crawler to access the Twitter API
    auth = tweepy.OAuthHandler(config['consumer_key'],
                               config['consumer_secret'])
    
    auth.set_access_token(config['access_token'],
                          config['access_token_secret'])

    # create and run the tweet crawler
    crawler = TweetCrawler(auth)
    
    # retrieve the arguments list for the crawler
    # args[0] == crawler mode (track, geo, or sample)
    # args[1], args[2], ... == arguments to relevant crawler
    args = sys.argv[1:]
    if len(args) == 0:
        raise RuntimeError('Missing crawler mode: track, geo, or sample')
    crawler_mode = args[0]
    
    # launch appropriate crawler based on the specified crawler_mode
    if crawler_mode == 'track':
        
        # list of topics to track (topic1 OR topic2 OR ... OR topicN)
        tracks = args[1:]
        print('Using proxy server at {}'.format(config.get('proxy_server')))
        print("Listening for Twitter stream about '{}'...".format(' OR '.join(tracks)))
        sys.stdout.flush()
        
        # gracefully handle Ctrl^C exit from tweet crawling process
        try:
            crawler.crawl_tracks(tracks)
        except KeyboardInterrupt:
            print("\nStopped tweet crawler for: '{}'".format(' OR '.join(tracks)))
        
    elif crawler_mode == 'geo':

        # list of geolocation bounding boxes to filter tweets
        # input format: [bottom-left-lon, bottom-left-lat,
        #                top-right-lon, top-right-lat, ...]
        locations = list(map(float, args[1:]))
        print('Using proxy server at {}'.format(config.get('proxy_server')))
        print("Listening for Tweets within bounding box: {}...".format(locations))
        sys.stdout.flush()
        
        # gracefully handle Ctrl^C exit from tweet crawling process
        try:
            crawler.crawl_geolocations(locations)
        except KeyboardInterrupt:
            print('\nStopped tweet crawler for bounding box: {}'.format(locations))
        
    elif crawler_mode == 'sample':
        
        langs = args[1:]
        print('Using proxy server at {}'.format(config.get('proxy_server')))
        print('Listening for random sample of tweets in languages: {}'.format(langs), flush=True)
        
        # gracefully handle Ctrl^C exit from tweet sampling process
        try:
            crawler.crawl_sample(languages=langs)
        except KeyboardInterrupt:
            print('\nStopped tweet sampler for tweets in languages: {}'.format(langs))
        
    else:

        raise RuntimeError('Invalid crawler mode specified: {}'.format(crawler_mode))

if __name__ == '__main__':
    main()
