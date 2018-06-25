def expand_tweet(status):
    '''Given a tweepy Status object, expands the text of the tweet
    
    The expanded full tweet (after text expansion) can be found
    in the full_tweet field of the saved MongoDB document
    '''
    data = status._json
    data['full_tweet'] = get_full_text(status)

def get_full_text(status):
    '''Given a tweepy Status object, returns the full text of the tweet'''
    data = status._json
    
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
