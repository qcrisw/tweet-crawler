from datetime import datetime

def expand_tweet(status):
    '''Given a tweepy Status object, expands the text of the tweet
    
    If the status object represents a retweet, then this 
    function sets "full_tweet" to the full text of the 
    retweeted tweet (i.e. the part after the "RT @handle:")
    
    If the status object is *not* a retweet, then this 
    function sets "full_tweet" to the full text of the 
    tweet body (by expanding any tweets > 140 characters)
    '''
    data = status._json
    data['full_tweet'] = get_full_text(status)

def get_full_text(status):
    '''Given a tweepy Status object, returns the full text of the tweet
    
    If the status object represents a retweet, then this function 
    will return the full text of the retweeted tweet (i.e. the part
    after the "RT @handle:")
    
    If the status object is *not* a retweet, then this function 
    will return the full text of the tweet body (expanding any tweets 
    with > 140 characters)
    '''
    data = status._json
    
    # retweet, any # of characters
    if is_retweet(status):
        data = data['retweeted_status']
        
        # retweeted tweet is > 140 characters
        if 'extended_tweet' in data:
            return data['extended_tweet']['full_text']
        
        # retweeted tweet is <= 140 characters
        else:
            return data['text']
    
    # original tweet, > 140 characters
    if 'extended_tweet' in data:
        return data['extended_tweet']['full_text']
    
    # original tweet, <= 140 characters
    else:
        return data['text']

def expand_hashtags(status):
    data = status._json
    data['full_hashtags'] = get_full_hashtags(status)

def get_full_hashtags(status):
    data = status._json
    
    # retweet, any # of characters
    if is_retweet(status):
        data = data['retweeted_status']
        
        # retweeted tweet is > 140 characters
        if 'extended_tweet' in data:
            return data['extended_tweet']['entities']['hashtags']
        
        # retweeted tweet is <= 140 characters
        else:
            return data['entities']['hashtags']
    
    # original tweet, > 140 characters
    if 'extended_tweet' in data:
        return data['extended_tweet']['entities']['hashtags']
    
    # original tweet, <= 140 characters
    else:
        return data['entities']['hashtags']

def expand_mentions(status):
    data = status._json
    data['full_mentions'] = get_full_mentions(status)

def get_full_mentions(status):
    data = status._json
    
    # retweet, any # of characters
    if is_retweet(status):
        data = data['retweeted_status']
        
        # retweeted tweet is > 140 characters
        if 'extended_tweet' in data:
            return data['extended_tweet']['entities']['user_mentions']
        
        # retweeted tweet is <= 140 characters
        else:
            return data['entities']['user_mentions']
    
    # original tweet, > 140 characters
    if 'extended_tweet' in data:
        return data['extended_tweet']['entities']['user_mentions']
    
    # original tweet, <= 140 characters
    else:
        return data['entities']['user_mentions']

def reformat_tweet(status):
    '''Given a status object from the Twitter API, reformat its date fields
    
    In particular, this function will convert the following raw string fields
    sent by the Twitter API into actual datetime (and int) objects:
    
    - created_at
    - user.created_at
    - retweeted_status.created_at
    - retweeted_status.user.created_at
    - timestamp_ms
    
    By doing this, we are able to better support a wider range of database 
    queries on date- and time-related fields
    '''
    data = status._json
    datetime_fmt = "%a %b %d %H:%M:%S %z %Y"
    
    data['created_at'] = datetime.strptime(data['created_at'], datetime_fmt)
    data['user']['created_at'] = datetime.strptime(data['user']['created_at'], datetime_fmt)
    data['timestamp_ms'] = int(data['timestamp_ms'])

    if is_retweet(status):
        retweet = data['retweeted_status']
        retweet['created_at'] = datetime.strptime(retweet['created_at'], datetime_fmt)
        retweet['user']['created_at'] = datetime.strptime(retweet['user']['created_at'], datetime_fmt)

def get_collection_name(status):
    '''Given a Status object, this function computes a collection name
    
    In particular, the "temporal sharding" of the database requires us to
    insert each Status object into the table/collection corresponding
    to the time at which the tweet was created.
    
    However, this function can be used to compute the collection name
    based on *any* attribute found in the source Status object
    '''
    created_at = status._json['created_at']
    return created_at.strftime('%Y_%m_%d')

def is_retweet(status):
    '''Given a tweepy Status object, returns whether or not it's a retweet'''
    data = status._json

    return 'retweeted_status' in data

def get_mongo_lang_code(twitter_lang_code):
    '''Converts from twitter- to mongo-supported language code
    
    In particular, this function maps the list language codes supported
    by the Twitter API (https://developer.twitter.com/en/docs/twitter-
    for-websites/twitter-for-websites-supported-languages/overview.html)
    into the corresponding language code supported by the *standard* (non-
    enterprise) edition of MongoDB (https://docs.mongodb.com/manual/reference
    /text-search-languages/#text-search-languages)
    
    If a language is not supported by non-enterprise MongoDB or is the 
    special value "und" (a.k.a. "undefined") the function will default to
    returning a value of "none"'''

    lang_code_map = {
        'da': 'da',
	'en': 'en',
	'ar': 'none',
	'bn': 'none',
	'cs': 'none',
	'de': 'de',
	'el': 'none',
	'es': 'es',
	'fa': 'none',
	'fi': 'fi',
	'fil': 'none',
	'fr': 'fr',
	'he': 'none',
	'hi': 'none',
	'hu': 'hu',
	'id': 'none',
	'it': 'it',
	'ja': 'none',
	'ko': 'none',
	'msa': 'none',
	'nl': 'nl',
	'no': 'nb',
	'pl': 'none',
	'pt': 'pt',
	'ro': 'ro',
	'ru': 'ru',
	'sv': 'sv',
	'th': 'none',
	'tr': 'tr',
	'uk': 'none',
	'ur': 'none',
	'vi': 'none',
	'zh-cn': 'none',
	'zh-tw': 'none',
	'und': 'none'
    }

    return lang_code_map.get(twitter_lang_code, 'none')
