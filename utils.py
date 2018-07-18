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

def is_retweet(status):
    '''Given a tweepy Status object, returns whether or not it's a retweet'''
    data = status._json

    return 'retweeted_status' in data
