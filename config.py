import os

# retrieve the crawler's configuration options
config = {
    "consumer_key": os.environ['TWITTER_CONSUMER_KEY'],
    "consumer_secret": os.environ['TWITTER_CONSUMER_SECRET'],
    "access_token": os.environ['TWITTER_ACCESS_TOKEN'],
    "access_token_secret": os.environ['TWITTER_ACCESS_TOKEN_SECRET'],
    "proxy_server": os.environ.get('CRAWLER_PROXY_IP')
}

# raise exception if any of the API keys above are not defined
for key in config:
    if config[key] == '':
        if key in {'consumer_key', 'consumer_secret',
                   'access_token', 'access_token_secret'}:
            
            raise RuntimeError('Key', '"{}"'.format(key), 'has not been set')
