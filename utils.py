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

def is_retweet(status):
    '''Given a tweepy Status object, returns whether or not it's a retweet'''
    data = status._json

    return 'retweeted_status' in data
