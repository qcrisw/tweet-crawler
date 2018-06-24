import os

# retrieve the crawler's configuration options
config = {
    "consumer_key": os.environ['TWITTER_CONSUMER_KEY'],
    "consumer_secret": os.environ['TWITTER_CONSUMER_SECRET'],
    "access_token": os.environ['TWITTER_ACCESS_TOKEN'],
    "access_token_secret": os.environ['TWITTER_ACCESS_TOKEN_SECRET']
}

# raise exception if any of the above are not defined
for key in config:
    if config[key] == '':
        raise RuntimeError('Key', '"{}"'.format(key), 'has not been set')
